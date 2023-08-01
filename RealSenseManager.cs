using System;
using System.Diagnostics;
using System.IO;

public class RealSenseManager
{   
    public event Action<string> ErrorOccurred;
    private string recordScript = "start_record.py";
    float StartTime;
    float EndTime;

    // 실행 중인 프로세스를 추적
    private Process currentProcess;

    public RealSenseManager();

    public float StartRecording(float currentTime)
    {
        currentProcess = RunPythonScript(recordScript);
        StartTime = currentTime;

        // 파이썬 스크립트의 에러 출력 확인
        currentProcess.ErrorDataReceived += (sender, e) => 
        {
            if (e.Data != null)
            {
                // 에러 출력을 에러 발생 이벤트로 전달
                OnErrorOccurred(e.Data);
            }
        };
        currentProcess.BeginErrorReadLine();

        string output = currentProcess.StandardOutput.ReadToEnd();

        float recordingStartTime;
        float timeDifference = 0.0;
        if (float.TryParse(output, out recordingStartTime)){
            timeDifference = recordingStartTime - invokeTime;
        }
        
        return timeDifference;
    }

    public void StopRecording()
    {
        if(currentProcess != null){
            currentProcess?.Kill();
            currentProcess = null;
        }
    }

    private Process RunPythonScript(string scriptPath)
    {
        var start = new ProcessStartInfo
        {
            FileName = "python",
            Arguments = $"\"{scriptPath}\"",
            UseShellExecute = false,
            RedirectStandardOutput = true,
            CreateNoWindow = true
        };

        var process = Process.Start(start);
        return process;
    }
    private void OnErrorOccurred(string message)
    {
        ErrorOccurred?.Invoke(message);
    }
    public void CheckForErrors()
    {
        if (File.Exists(errorFile))
        {
            string errorMessage = File.ReadAllText(errorFile);
            OnErrorOccurred(errorMessage);
            File.Delete(errorFile);
        }
    }

}
