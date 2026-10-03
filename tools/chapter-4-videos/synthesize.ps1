param([Parameter(Mandatory=$true)][string]$RequestPath)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
Add-Type -ReferencedAssemblies System.Speech -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Speech.Synthesis;
using System.Speech.AudioFormat;

public class ChapterFourSpeechWord {
    public string text { get; set; }
    public long offset { get; set; }
}

public static class ChapterFourOfflineSpeech {
    public static List<ChapterFourSpeechWord> Export(string text, string voice, string path) {
        var words = new List<ChapterFourSpeechWord>();
        using (var synth = new SpeechSynthesizer()) {
            synth.SelectVoice(voice);
            synth.Rate = 0;
            // David Desktop's native clock is 16 kHz. Higher output rates can
            // make System.Speech report positions on the wrong sample clock.
            synth.SetOutputToWaveFile(path, new SpeechAudioFormatInfo(
                16000, AudioBitsPerSample.Sixteen, AudioChannel.Mono));
            synth.SpeakProgress += (sender, e) => words.Add(new ChapterFourSpeechWord {
                text = e.Text, offset = e.AudioPosition.Ticks
            });
            synth.Speak(text);
            synth.SetOutputToNull();
        }
        return words;
    }
}
'@

$chapterFourRequest = Get-Content -LiteralPath $RequestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$chapterFourWords = [ChapterFourOfflineSpeech]::Export(
    $chapterFourRequest.text, $chapterFourRequest.voice, $chapterFourRequest.wav)
if ($chapterFourWords.Count -eq 0) { throw 'No offline word timings returned' }
ConvertTo-Json -InputObject @($chapterFourWords) -Depth 4 |
    Set-Content -LiteralPath $chapterFourRequest.events -Encoding UTF8
