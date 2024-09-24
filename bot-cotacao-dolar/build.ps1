$exclude = @("venv", "bot-cotacao-dolar.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "bot-cotacao-dolar.zip" -Force