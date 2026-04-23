# Skills 定期同步任务

# 创建每日检查任务（上午 9:00）
$action = New-ScheduledTaskAction -Execute "D:\Personal\skills\check_update.bat" -WorkingDirectory "D:\Personal\skills"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -AllowStartIfOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName "Skills-Sync" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "检查 anthropics/skills 更新并同步" -Force

Write-Host "✅ 定时任务创建成功!"