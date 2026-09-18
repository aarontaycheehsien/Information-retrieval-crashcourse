param([string]$WorkbookPath = (Join-Path $PSScriptRoot '..\downloads\evaluation-worked-example.xlsx'))
# Native Excel verification. Opens only a disposable copy in a separate hidden instance.
$ErrorActionPreference = 'Stop'
$source = (Resolve-Path -LiteralPath $WorkbookPath).Path
$scratch = Join-Path ([IO.Path]::GetTempPath()) ('evaluation-kit-' + [guid]::NewGuid() + '.xlsx')
Copy-Item -LiteralPath $source -Destination $scratch
$excel = $null
$book = $null
$assertions = 0
function Assert-Value($Sheet, $Cell, $Expected) {
    $actual = $Sheet.Range($Cell).Value2
    if ($Expected -is [double] -or $Expected -is [int]) {
        if ($null -eq $actual -or [math]::Abs([double]$actual - $Expected) -gt 0.0000001) { throw "$($Sheet.Name)!$Cell expected $Expected, got $actual" }
    } elseif ([string]$actual -ne [string]$Expected) { throw "$($Sheet.Name)!$Cell expected '$Expected', got '$actual'" }
    $script:assertions++
}
function Recalculate { $excel.CalculateFullRebuild() }
function Reset-Inputs {
    $queries.Range('A6:S55').Value2 = $baseQueries
    $records.Range('A6:H105').Value2 = $baseRecords
    $comparison.Range('B4').Value2 = 10
    $comparison.Range('A6:Q55').Formula = $baseComparisonFormulas
    Recalculate
}
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $excel.AskToUpdateLinks = $false
    $excel.AutomationSecurity = 3
    $book = $excel.Workbooks.Open($scratch, 0, $false)
    $comparison = $book.Worksheets.Item('Comparison')
    $queries = $book.Worksheets.Item('Queries')
    $records = $book.Worksheets.Item('Records')
    $baseQueries = $queries.Range('A6:S55').Value2
    $baseRecords = $records.Range('A6:H105').Value2
    $baseComparisonFormulas = $comparison.Range('A6:Q55').Formula
    Recalculate
    Assert-Value $comparison C6 'Ready'
    Assert-Value $comparison I6 0.2
    Assert-Value $comparison J6 0.6
    Assert-Value $comparison K6 0.4
    Assert-Value $comparison L6 5
    Assert-Value $comparison M6 1
    Assert-Value $comparison N6 3
    Assert-Value $comparison O6 0.2
    Assert-Value $comparison P6 0.6
    Assert-Value $comparison Q6 0.4
    $comparison.Range('B4').Value2 = 20
    Recalculate
    Assert-Value $comparison I6 0.5
    Assert-Value $comparison J6 0.5
    Assert-Value $comparison O6 1
    Assert-Value $comparison P6 1

    Reset-Inputs
    $records.Range('D7').Value2 = 'Not relevant' # B: relevant in both top tens, not a seed.
    Recalculate
    Assert-Value $comparison I6 0.1
    Assert-Value $comparison J6 0.5
    Assert-Value $comparison O6 0.2
    Reset-Inputs
    $records.Range('G8').Value2 = 2 # Swap C (relevant seed) with K.
    $records.Range('G16').Value2 = 11
    Recalculate
    Assert-Value $comparison I6 0.3
    Assert-Value $comparison O6 0.4

    Reset-Inputs
    $records.Range('D7').ClearContents() | Out-Null
    Recalculate
    Assert-Value $comparison C6 'Judge all pooled records at k'
    Assert-Value $comparison I6 ''
    Assert-Value $comparison J6 ''
    Assert-Value $comparison O6 0.2 # Seeds do not depend on new pooled judgements.
    Reset-Inputs
    $records.Range('D13').ClearContents() | Out-Null # H is below both cutoffs.
    Recalculate
    Assert-Value $comparison C6 'Ready'
    Assert-Value $comparison I6 0.2
    Reset-Inputs
    $records.Range('F6:F25').Value2 = 'No'
    Recalculate
    Assert-Value $comparison I6 0.2
    Assert-Value $comparison O6 'No seeds specified'
    Assert-Value $comparison Q6 ''
    Reset-Inputs
    $records.Range('A26').Value2 = 'EX01'
    $records.Range('B26').Value2 = 'U'
    $records.Range('D26').Value2 = 'Relevant'
    $records.Range('F26').Value2 = 'Yes'
    Recalculate
    Assert-Value $comparison L6 6
    Assert-Value $comparison O6 (1.0/6)
    Assert-Value $comparison P6 0.5

    Reset-Inputs
    $records.Range('A6:H105').ClearContents() | Out-Null
    $queries.Range('I6').Value2 = 10
    $queries.Range('L6').Value2 = 10
    $queries.Range('J6').Value2 = 3
    $queries.Range('M6').Value2 = 3
    foreach ($row in 6..8) {
        $records.Cells.Item($row,1).Value2 = 'EX01'
        $records.Cells.Item($row,2).Value2 = [string]('S' + $row)
        $records.Cells.Item($row,4).Value2 = $(if ($row -lt 8) { 'Relevant' } else { 'Not relevant' })
        $records.Cells.Item($row,6).Value2 = 'No'
        $records.Cells.Item($row,7).Value2 = [double]($row - 5)
        $records.Cells.Item($row,8).Value2 = [double]($row - 5)
    }
    Recalculate
    Assert-Value $comparison C6 'Ready'
    Assert-Value $comparison D6 3
    Assert-Value $comparison I6 0.2
    $records.Range('G8').Value2 = 4 # Preserve a gap caused by a duplicate position.
    Recalculate
    Assert-Value $comparison C6 'Ready'
    Assert-Value $comparison I6 0.2
    $comparison.Range('B4').Value2 = 20
    Recalculate
    Assert-Value $comparison C6 'Extend capture to the selected cutoff'
    Assert-Value $comparison I6 ''
    $comparison.Range('B4').Value2 = 10
    $records.Range('A6:H105').ClearContents() | Out-Null
    $queries.Range('J6').Value2 = 0
    $queries.Range('M6').Value2 = 0
    Recalculate
    Assert-Value $comparison C6 'Ready'
    Assert-Value $comparison I6 0
    Assert-Value $comparison J6 0
    $queries.Range('K6').ClearContents() | Out-Null
    Recalculate
    Assert-Value $comparison C6 'Confirm both captures complete'
    Assert-Value $comparison I6 ''

    foreach ($case in @(
        @('B7','A','Duplicate record ID'),
        @('G7',1,'Duplicate rank'),
        @('G7',-1,'Invalid rank'),
        @('G7',1.5,'Invalid rank'),
        @('G7','two','Invalid rank'),
        @('D7','Maybe','Invalid judgement'),
        @('F7','Sometimes','Invalid seed flag'),
        @('D6','Not relevant','Seed marked not relevant'),
        @('B7','','Missing record ID')
    )) {
        Reset-Inputs
        if ($case[1] -eq '') { $records.Range($case[0]).ClearContents() | Out-Null }
        else { $records.Range($case[0]).Value2 = $case[1] }
        Recalculate
        $row = $(if ($case[0] -eq 'D6') { 6 } else { 7 })
        Assert-Value $records "I$row" $case[2]
        Assert-Value $comparison I6 ''
        Assert-Value $comparison O6 ''
    }
    Reset-Inputs
    $queries.Range('C6').ClearContents() | Out-Null
    Recalculate
    Assert-Value $comparison C6 'Write relevance criteria'
    Assert-Value $comparison I6 ''
    Reset-Inputs
    $queries.Range('J6').Value2 = 19
    Recalculate
    Assert-Value $comparison C6 'Captured counts disagree with Records'
    Reset-Inputs
    $queries.Range('I6').Value2 = 10
    Recalculate
    Assert-Value $comparison C6 'Rank exceeds recorded capture depth'
    Reset-Inputs
    $records.Range('A6').Value2 = 'Other'
    Recalculate
    Assert-Value $comparison N4 1
    Assert-Value $comparison C6 'Fix unassigned Records rows'
    Reset-Inputs
    $records.Range('A6').ClearContents() | Out-Null
    Recalculate
    Assert-Value $comparison N4 1
    Assert-Value $comparison I6 ''
    Reset-Inputs
    $records.Range('B6').Value2 = 'literal*id?'
    Recalculate
    Assert-Value $records I6 'OK'
    Assert-Value $comparison I6 0.2

    # A second query gets independent labels and seeds for the same record ID.
    Reset-Inputs
    $queries.Range('A6:S6').Copy($queries.Range('A7:S7')) | Out-Null
    $queries.Range('A7').Value2 = 'EX02'
    $queries.Range('J7').Value2 = 1
    $queries.Range('M7').Value2 = 1
    $records.Range('A26').Value2 = 'EX02'
    $records.Range('B26').Value2 = 'A'
    $records.Range('D26').Value2 = 'Not relevant'
    $records.Range('F26').Value2 = 'No'
    $records.Range('G26').Value2 = 1
    $records.Range('H26').Value2 = 1
    Recalculate
    Assert-Value $comparison C7 'Ready'
    Assert-Value $comparison I7 0
    Assert-Value $comparison I6 0.2

    # Sort complete tables independently; query identity must keep scores aligned.
    $recordSort = $records.ListObjects.Item('RecordData').Sort
    $recordSort.SortFields.Clear()
    [void]$recordSort.SortFields.Add($records.Range('B6:B105'),0,2)
    $recordSort.Header = 1
    $recordSort.Apply()
    Recalculate
    Assert-Value $comparison I6 0.2
    Assert-Value $comparison I7 0
    $querySort = $queries.ListObjects.Item('QueryData').Sort
    $querySort.SortFields.Clear()
    [void]$querySort.SortFields.Add($queries.Range('A6:A55'),0,2)
    $querySort.Header = 1
    $querySort.Apply()
    Recalculate
    Assert-Value $comparison A6 'EX02'
    Assert-Value $comparison I6 0
    Assert-Value $comparison A7 'EX01'
    Assert-Value $comparison I7 0.2
    $comparisonSort = $comparison.ListObjects.Item('ComparisonData').Sort
    $comparisonSort.SortFields.Clear()
    [void]$comparisonSort.SortFields.Add($comparison.Range('J6:J55'),0,2)
    $comparisonSort.Header = 1
    $comparisonSort.Apply()
    Recalculate
    # Excel can sort formula-empty rows ahead of numbers. Locate the two IDs,
    # then verify that the scores and validation still belong to those IDs.
    $found = 0
    foreach ($sortedRow in 6..55) {
        $sortedID = $comparison.Range("A$sortedRow").Value2
        if ($sortedID -eq 'EX01') {
            Assert-Value $comparison "I$sortedRow" 0.2
            Assert-Value $comparison "C$sortedRow" 'Ready'
            $found++
        } elseif ($sortedID -eq 'EX02') {
            Assert-Value $comparison "I$sortedRow" 0
            Assert-Value $comparison "C$sortedRow" 'Ready'
            $found++
        }
    }
    if ($found -ne 2) { throw "Expected two populated queries after sorting; found $found" }

    # Expand the Excel table and use the documented copy-down workflow.
    Reset-Inputs
    $table = $records.ListObjects.Item('RecordData')
    $added = $table.ListRows.Add()
    $addedRow = $added.Range.Row
    $records.Range("I$($addedRow-1):Q$($addedRow-1)").Copy($records.Range("I${addedRow}:Q${addedRow}")) | Out-Null
    $records.Range("A$addedRow").Value2 = 'EX01'
    $records.Range("B$addedRow").Value2 = 'New missed seed'
    $records.Range("D$addedRow").Value2 = 'Relevant'
    $records.Range("F$addedRow").Value2 = 'Yes'
    Recalculate
    Assert-Value $records "I$addedRow" 'OK'
    Assert-Value $comparison L6 6
    Assert-Value $comparison O6 (1.0/6)
    $added.Delete()

    # Extend both query and comparison tables past fifty rows.
    Reset-Inputs
    $queryAdded = $queries.ListObjects.Item('QueryData').ListRows.Add()
    $comparisonAdded = $comparison.ListObjects.Item('ComparisonData').ListRows.Add()
    $newRow = $queryAdded.Range.Row
    $queries.Range('A6:U6').Copy($queries.Range("A${newRow}:U${newRow}")) | Out-Null
    $queries.Range("A$newRow").Value2 = 'EX51'
    $queries.Range("J$newRow").Value2 = 0
    $queries.Range("M$newRow").Value2 = 0
    $comparison.Range('A6:Q6').Copy($comparison.Range("A${newRow}:Q${newRow}")) | Out-Null
    Recalculate
    Assert-Value $comparison "A$newRow" 'EX51'
    Assert-Value $comparison "C$newRow" 'Ready'
    Assert-Value $comparison "I$newRow" 0
    # Native save/reopen verifies formulas and state persist.
    $book.Save()
    $book.Close($false)
    $book = $excel.Workbooks.Open($scratch,0,$true)
    $comparison = $book.Worksheets.Item('Comparison')
    Recalculate
    Assert-Value $comparison I6 0.2
    Assert-Value $comparison "I$newRow" 0
    Write-Output "PASS: $assertions native Excel assertions; scoring, missing data, input changes, extension and save/reopen."
} finally {
    if ($book) { $book.Close($false) }
    if ($excel) { $excel.Quit() }
    foreach ($obj in @($comparison,$queries,$records,$table,$added,$queryAdded,$comparisonAdded,$book,$excel)) {
        if ($null -ne $obj -and [Runtime.InteropServices.Marshal]::IsComObject($obj)) { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($obj) }
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
    # Only the exact disposable file created above is removed.
    if (Test-Path -LiteralPath $scratch) { Remove-Item -LiteralPath $scratch }
}
