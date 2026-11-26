-- Book filter: renders the Markdown conventions in data/markdown-mapping.json
-- and reviews/markdown-mapping-spec.md as the textbook's exact HTML.
--
-- Run by tools/markdown/build_md.py, never on its own: the Python build
-- expands the placeholder comments this filter leaves (stage maps, chapter
-- navigation) and collects footnote definitions.
--
-- Output that existing generators read with regular expressions keeps the
-- book's attribute order and spacing: asset labels (class before id,
-- "Table 0.0 — " / "Figure 0.0"), the table-wrap/table adjacency, headings.
-- maintain.py replaces the 0.0 placeholders and adds the asset ids.

local stringify = pandoc.utils.stringify
local meta_kind = 'chapter'

local WRITER = { wrap_text = 'wrap-none' }

local function inlines_html(inlines)
  return (pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), 'html5', WRITER):gsub('\n$', ''))
end

local function blocks_html(blocks)
  return (pandoc.write(pandoc.Pandoc(blocks), 'html5', WRITER):gsub('\n$', ''))
end

local function esc(s)
  return (s:gsub('&', '&amp;'):gsub('"', '&quot;'):gsub('<', '&lt;'):gsub('>', '&gt;'))
end

local function raw(s) return pandoc.RawBlock('html', s) end
local function rawi(s) return pandoc.RawInline('html', s) end

local function has(el, cls)
  for _, c in ipairs(el.classes) do if c == cls then return true end end
  return false
end

local function others(el, skip)
  local out = {}
  for _, c in ipairs(el.classes) do if c ~= skip then out[#out + 1] = c end end
  return out
end

-- Attribute string in a fixed order, skipping absent values.
local function attrs(list)
  local out = {}
  for _, kv in ipairs(list) do
    if kv[2] ~= nil then out[#out + 1] = string.format(' %s="%s"', kv[1], esc(kv[2])) end
  end
  return table.concat(out)
end

local function single_para(div)
  if #div.content == 1 and (div.content[1].t == 'Para' or div.content[1].t == 'Plain') then
    return div.content[1]
  end
  return nil
end

local function concat(...)
  local out = pandoc.List()
  for _, part in ipairs({ ... }) do
    if part.t then out:insert(part) else out:extend(part) end
  end
  return out
end

------------------------------------------------------------------------
-- Inline conventions

local ELEMENT_SPANS = { var = true, small = true, b = true, output = true }
local footnotes = {}

local function Span(sp)
  if #sp.classes == 1 and ELEMENT_SPANS[sp.classes[1]] and sp.identifier == '' then
    local tag = sp.classes[1]
    return concat(rawi('<' .. tag .. '>'), sp.content, rawi('</' .. tag .. '>'))
  end
  if #sp.classes == 1 and sp.classes[1] == 'verdict' and #sp.content == 1 and sp.content[1].t == 'Emph' then
    return concat(rawi('<em class="verdict">'), sp.content[1].content, rawi('</em>'))
  end
end

local function Note(note)
  -- The build pre-pass starts each definition with []{.fn-name name=NAME}.
  local first = note.content[1]
  local name
  if first and first.content and first.content[1] and first.content[1].t == 'Span' then
    name = first.content[1].attributes['name']
  end
  if not name then error('footnote without a name; was the build pre-pass skipped?') end
  first.content:remove(1)
  footnotes[#footnotes + 1] = { name = name, blocks = note.content }
  return rawi(string.format('<sup id="fnref:%s"><a class="footnote-ref" href="#fn:%s">0</a></sup>', name, name))
end

local function Math(m)
  if m.mathtype == 'InlineMath' then return rawi('\\(' .. m.text .. '\\)') end
  return rawi('$$\n' .. m.text:gsub('^\n', ''):gsub('\n$', '') .. '\n$$')
end

------------------------------------------------------------------------
-- Block conventions

local function Header(h)
  if h.level == 2 then
    if meta_kind ~= 'backsection' then return nil end
  elseif h.level ~= 3 then
    return nil
  end
  if h.identifier == '' then error('h' .. h.level .. ' without an id: ' .. stringify(h.content)) end
  local tag = 'h' .. h.level
  local extra = ''
  if #h.classes > 0 then extra = ' class="' .. table.concat(h.classes, ' ') .. '"' end
  return raw(string.format('<%s id="%s"%s>%s<a aria-label="Link to %s" class="heading-anchor" href="#%s">#</a></%s>',
    tag, h.identifier, extra, inlines_html(h.content), esc(stringify(h.content)), h.identifier, tag))
end

local function OrderedList(ol)
  ol.listAttributes = pandoc.ListAttributes(ol.listAttributes.start, 'DefaultStyle', 'DefaultDelim')
  return ol
end

local function cell_html(cell)
  if #cell.contents == 0 then return '' end
  if #cell.contents == 1 and (cell.contents[1].t == 'Plain' or cell.contents[1].t == 'Para') then
    return inlines_html(cell.contents[1].content)
  end
  return blocks_html(cell.contents)
end

local function Table(tbl)
  local caption = tbl.caption.long
  if #caption ~= 1 then error('every table needs a one-paragraph caption') end
  local out = { string.format('<p class="asset-label">Table 0.0 — %s</p><div class="table-wrap"><table%s>',
    inlines_html(caption[1].content),
    (#tbl.classes > 0) and (' class="' .. table.concat(tbl.classes, ' ') .. '"') or '') }
  local head = {}
  for _, row in ipairs(tbl.head.rows) do
    local cells = {}
    for _, cell in ipairs(row.cells) do cells[#cells + 1] = '<th>' .. cell_html(cell) .. '</th>' end
    head[#head + 1] = '<tr>' .. table.concat(cells) .. '</tr>'
  end
  if #head > 0 then out[#out + 1] = '<thead>' .. table.concat(head) .. '</thead>' end
  out[#out + 1] = '<tbody>'
  for _, body in ipairs(tbl.bodies) do
    for _, row in ipairs(body.body) do
      local cells = {}
      for _, cell in ipairs(row.cells) do cells[#cells + 1] = '<td>' .. cell_html(cell) .. '</td>' end
      out[#out + 1] = '<tr>' .. table.concat(cells) .. '</tr>'
    end
  end
  out[#out + 1] = '</tbody>'
  out[#out + 1] = '</table></div>'
  return raw(table.concat(out, '\n'))
end

-- A PNG with a .960.webp sibling gets the book's responsive srcset; the
-- WebP entry percent-encodes commas because srcset uses them as separators.
-- Converter and filter share this rule (html_to_md.derive_srcset).
local DEFAULT_SIZES = '(max-width: 800px) 100vw, 760px'

local function derived_srcset(src, width)
  if not width or not src:match('%.png$') then return nil end
  local webp = src:gsub('%.png$', ''):gsub(',', '%%2C') .. '.960.webp'
  local f = io.open(ROOT_DIR .. '/' .. pandoc.path.normalize(webp:gsub('%%2C', ','):gsub('%%20', ' ')), 'r')
  if not f then return nil end
  f:close()
  return webp .. ' 960w, ' .. src .. ' ' .. width .. 'w'
end

local function image_html(img)
  local a = img.attributes
  local srcset = a['srcset'] or derived_srcset(img.src, a['width'])
  local sizes = a['sizes'] or (srcset and DEFAULT_SIZES or nil)
  if a['srcset'] == 'none' then srcset, sizes = nil, a['sizes'] end
  return string.format('<img%s>', attrs({
    { 'loading', a['loading'] or 'lazy' }, { 'width', a['width'] }, { 'height', a['height'] },
    { 'srcset', srcset }, { 'sizes', sizes }, { 'alt', stringify(img.caption) }, { 'src', img.src },
  }))
end

local function include(div)
  local path = div.attributes['src']
  local f = assert(io.open(BOOK_DIR .. '/' .. path, 'r'), 'cannot read include ' .. path)
  local text = f:read('a'); f:close()
  return raw((text:gsub('\n$', '')))
end

local function figure_body(block)
  if block.t == 'Para' and #block.content == 1 and block.content[1].t == 'Image' then
    return raw(image_html(block.content[1]))
  end
  return block
end

local function Figure(div)
  local key = div.attributes['key']
  local title = div.content[1]
  if not key or not title or title.t ~= 'Para' then error('figure needs key= and a title paragraph') end
  local last = div.content[#div.content]
  if not (last.t == 'Div' and has(last, 'caption')) then error('figure ' .. key .. ' needs a ::: caption block last') end
  local tag = div.attributes['tag'] or 'figure'
  local classes = { 'ir-figure' }
  for _, c in ipairs(others(div, 'figure')) do classes[#classes + 1] = c end
  local title_id = div.attributes['title-id'] or (key .. '-title')
  if title_id == '' then title_id = nil end
  local labelled = div.attributes['aria-labelledby'] or title_id
  local out = pandoc.List({ raw(string.format('<%s%s>', tag, attrs({
      { 'class', table.concat(classes, ' ') }, { 'role', div.attributes['role'] }, { 'aria-labelledby', labelled } }))
    .. '\n' .. string.format('<p class="figure-title"%s>%s</p>', attrs({ { 'id', title_id } }), inlines_html(title.content))) })
  for i = 2, #div.content - 1 do out:insert(figure_body(div.content[i])) end
  local cap = single_para(last)
  if tag == 'figure' then
    if not cap then error('figure ' .. key .. ': caption must be one paragraph') end
    out:insert(raw(string.format('<figcaption%s><span class="asset-label-inline">Figure 0.0</span> %s</figcaption>\n</%s>',
      attrs({ { 'id', last.attributes['id'] or (last.identifier ~= '' and last.identifier or nil) } }),
      inlines_html(cap.content), tag)))
  else
    out:extend(last.content)
    out:insert(raw('</' .. tag .. '>'))
  end
  return out
end

-- <aside> types. The label paragraph and accessible name are derived;
-- attributes on the div override the derivation.
local ASIDES = {
  ['common-confusion'] = true, ['practice-callout'] = true, ['question-callout'] = true,
  ['orientation'] = true, ['distinction-map'] = true, ['part-recap'] = true,
  ['ai-disclosure-notice'] = true,
}

local function Aside(div, cls)
  local a = div.attributes
  local label = a['label']
  local first = div.content[1]
  local labelled = a['aria-labelledby']
  if not labelled and not a['aria-label'] and first and first.t == 'Header' and first.identifier ~= '' then
    labelled = first.identifier
  end
  local tag = a['tag'] or 'aside'
  local open = string.format('<%s%s>', tag, attrs({ { 'class', cls }, { 'id', div.identifier ~= '' and div.identifier or nil },
    { 'aria-labelledby', labelled }, { 'aria-label', a['aria-label'] } }))
  if label then
    open = open .. '\n' .. string.format('<p class="%s">%s</p>', a['label-class'] or (cls .. '-label'), esc(label))
  end
  return concat(raw(open), div.content, raw('</' .. tag .. '>'))
end

local PARA_CLASSES = {
  ['chapter-transition'] = true, ['key-distinction-label'] = true, ['exercise-deliverable'] = true,
  ['worked-note'] = true, ['ir-figure-note'] = true, ['practice-callout'] = true, ['equation-scroll'] = true,
}
local BLOCK_CLASS_TRANSFER = { ['pull-quote'] = 'BlockQuote', ['stage-key'] = 'DefinitionList' }

local function Div(div)
  local cls = div.classes[1]
  if has(div, 'caption') or has(div, 'chapter-orient') then return nil end
  if has(div, 'figure') then return Figure(div) end
  if has(div, 'include') then return include(div) end
  if cls == 'legacy-anchor' and #div.content == 0 then
    return raw(string.format('<span id="%s" class="legacy-anchor"></span>', div.identifier))
  end
  if cls == 'stage-map' then
    local a = div.attributes
    return raw(string.format('<!-- STAGE MAP on="%s" controller="%s" label="%s" -->',
      a['on'] or '', a['controller'] or 'off', esc(a['label'] or '')))
  end
  if cls == 'details' then
    local summary = div.content[1]
    local rest = pandoc.List()
    for i = 2, #div.content do rest:insert(div.content[i]) end
    local extra = others(div, 'details')
    return concat(raw(string.format('<details%s><summary>%s</summary>',
      attrs({ { 'class', #extra > 0 and table.concat(extra, ' ') or nil } }), inlines_html(summary.content))), rest, raw('</details>'))
  end
  if cls == 'self-check' then
    local dl = div.content[1]
    if #div.content ~= 1 or dl.t ~= 'DefinitionList' then error('self-check must hold one definition list') end
    local out = pandoc.List({ raw('<section class="self-check" aria-label="Questions on this chapter"><p class="self-check-label">Check yourself</p>') })
    for _, item in ipairs(dl.content) do
      out:insert(raw('<details class="self-check-q"><summary>' .. inlines_html(item[1]) .. '</summary>'))
      for _, def in ipairs(item[2]) do out:extend(def) end
      out:insert(raw('</details>'))
    end
    out:insert(raw('</section>'))
    return out
  end
  if cls == 'chapter-close' then
    return concat(raw(string.format('<aside class="chapter-close" aria-label="%s"><p class="chapter-close-label">%s</p>',
      esc(div.attributes['aria-label'] or 'Chapter summary'), esc(div.attributes['label'] or 'What this chapter established'))),
      div.content, raw('</aside>'))
  end
  if cls and ASIDES[cls] then return Aside(div, cls) end
  if cls and BLOCK_CLASS_TRANSFER[cls] and #div.content == 1 and div.content[1].t == BLOCK_CLASS_TRANSFER[cls] then
    local inner = blocks_html(div.content):gsub('^<(%w+)', '<%1 class="' .. cls .. '"', 1)
    return raw(inner)
  end
  local para = single_para(div)
  if para and ((cls and PARA_CLASSES[cls] and #div.classes == 1) or (#div.classes == 0 and div.identifier ~= '')) then
    return raw(string.format('<p%s>%s</p>', attrs({ { 'class', cls }, { 'id', div.identifier ~= '' and div.identifier or nil } }),
      inlines_html(para.content)))
  end
  return nil
end

------------------------------------------------------------------------
-- Whole-file assembly

local function Pandoc(doc)
  local m = doc.meta
  local kind = stringify(m.kind or 'chapter')
  local blocks = doc.blocks
  local out = pandoc.List()
  if kind == 'chapter' or kind == 'appendix' or kind == 'backsection' then
    local key = stringify(m.key)
    local classes = ({ chapter = 'chapter', appendix = 'chapter appendix', backsection = 'chapter backsection' })[kind]
    local open = string.format('<section class="%s" id="sec-%s">', classes, key)
    for _, anchor in ipairs(m.legacy_anchors or {}) do
      open = open .. string.format('<span id="%s" class="legacy-anchor"></span>', stringify(anchor))
    end
    local i = 1
    local title = blocks[i]
    if not (title and title.t == 'Header' and title.level == 2 and title.identifier == key) then
      error('first block must be ## Title {#' .. key .. '}')
    end
    local head = open .. '<header class="chapter-head">'
      .. string.format('<p class="chapter-eyebrow">%s</p>', esc(stringify(m.eyebrow)))
      .. (m.meta and string.format('<p class="chapter-meta">%s</p>', esc(stringify(m.meta))) or '')
      .. string.format('<h2 id="%s">%s</h2>', key, inlines_html(title.content))
    if m.question then
      head = head .. '<p class="chapter-question"><span>Central question</span>' .. inlines_html(m.question) .. '</p>'
    end
    out:insert(raw(head))
    i = i + 1
    while blocks[i] and ((blocks[i].t == 'RawBlock' and blocks[i].text:match('^<!%-%- STAGE MAP'))
        or (blocks[i].t == 'Div' and has(blocks[i], 'chapter-orient'))) do
      out:insert(blocks[i]); i = i + 1
    end
    out:insert(raw('</header>'))
    for j = i, #blocks do out:insert(blocks[j]) end
    out:insert(raw('<!-- CHAPTER NAV -->'))
    out:insert(raw('</section>'))
  else
    out = blocks
  end
  if #footnotes > 0 then
    out:insert(raw('<!-- FOOTNOTE DEFINITIONS -->'))
    for _, fn in ipairs(footnotes) do
      -- Backlink at the end of the last paragraph, after a no-break space.
      -- renumber_footnotes.py sets the number in its title.
      local last = fn.blocks[#fn.blocks]
      if not last or last.t ~= 'Para' then error('footnote ' .. fn.name .. ' must end with a paragraph') end
      last.content:insert(pandoc.Str('\u{a0}'))
      last.content:insert(rawi(string.format(
        '<a class="footnote-backref" href="#fnref:%s" title="Jump back to footnote 0 in the text">↩</a>', fn.name)))
      out:insert(raw(string.format('<li id="fn:%s">', fn.name)))
      out:extend(fn.blocks)
      out:insert(raw('</li>'))
    end
  end
  return pandoc.Pandoc(out, m)
end

BOOK_DIR = os.getenv('BOOK_DIR') or 'book'
ROOT_DIR = os.getenv('ROOT_DIR') or '.'

return {
  { Meta = function(m) meta_kind = stringify(m.kind or 'chapter') end },
  { Span = Span, Note = Note, Math = Math },
  { Header = Header, OrderedList = OrderedList, Table = Table, Div = Div },
  { Pandoc = Pandoc },
}
