param([Parameter(Mandatory=$true)][string]$RequestPath)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
Add-Type -ReferencedAssemblies System.Speech -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Speech.Synthesis;
using System.Speech.AudioFormat;

public class ChapterElevenSpeechWord {
    public string text { get; set; }
    public long offset { get; set; }
}

public static class ChapterElevenOfflineSpeech {
    public static List<ChapterElevenSpeechWord> Export(string text, string voice, int rate, string path) {
        var words = new List<ChapterElevenSpeechWord>();
        using (var synth = new SpeechSynthesizer()) {
            synth.SelectVoice(voice);
            synth.Rate = rate;
            // Hazel Desktop's native clock is 16 kHz. Higher output rates can
            // make System.Speech report positions on the wrong sample clock.
            synth.SetOutputToWaveFile(path, new SpeechAudioFormatInfo(
                16000, AudioBitsPerSample.Sixteen, AudioChannel.Mono));
            synth.SpeakProgress += (sender, e) => words.Add(new ChapterElevenSpeechWord {
                text = e.Text, offset = e.AudioPosition.Ticks
            });
            synth.Speak(text);
            synth.SetOutputToNull();
        }
        return words;
    }
}
'@

$chapterElevenRequest = Get-Content -LiteralPath $RequestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$chapterElevenWords = [ChapterElevenOfflineSpeech]::Export(
    $chapterElevenRequest.text, $chapterElevenRequest.voice, $chapterElevenRequest.rate, $chapterElevenRequest.wav)
if ($chapterElevenWords.Count -eq 0) { throw 'No offline word timings returned' }
ConvertTo-Json -InputObject @($chapterElevenWords) -Depth 4 |
    Set-Content -LiteralPath $chapterElevenRequest.events -Encoding UTF8
