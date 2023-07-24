param([string]$tag, [string]$user, [string]$repo, [string]$file)

function Upload([int]$releaseID, [string]$file)
{
    $fileName = Split-Path $file -Leaf
    if ([System.IO.Path]::GetExtension($file) -eq ".zip")
    {
        $header = $auth + @{"Content-Type"="application/zip"}
    }
    else
    {
        $header = $auth + @{"Content-Type"="application/x-msdownload"}
    }

    $response = Invoke-RestMethod -Headers $header -Method Post -InFile $file -Uri https://uploads.github.com/repos/$user/$repo/releases/$releaseID/assets?name=$fileName
}

function Delete([int]$releaseID, [string]$file)
{
    $fileName = Split-Path $file -Leaf
    $id = 0
    $assets = Invoke-WebRequest -Headers $auth -Uri https://api.github.com/repos/$user/$repo/releases/$releaseID/assets
    if ($null -eq $assets)
    {
      return 0
    }
    ConvertFrom-Json $assets.Content | Where-Object {$_.name -eq $fileName} | ForEach-Object {
        $id = $_.id
    }
    if ($id -ne 0)
    {
        Write-Host "Deleting Existing asset"
        Invoke-WebRequest -Headers $auth -Method DELETE -Uri https://api.github.com/repos/$user/$repo/releases/assets/$id
    }
}

function FindRelease([string] $tag)
{
    $releaseID = 0
    $releases = Invoke-WebRequest -Headers $auth -Uri https://api.github.com/repos/$user/$repo/releases
    if ($null -eq $releases)
    {
        return 0
    }

    ConvertFrom-Json $releases.Content | Where-Object {$_.tag_name -eq $tag} | ForEach-Object {
        $releaseID = $_.id
    }
    #Write-Host $releaseID
    return $releaseID
}

function CreateRelease([string]$tag)
{
    $release = ConvertTo-Json @{"tag_name"=$tag; "name"=$tag; "body"=""; "draft"=$FALSE; "prerelease"=$FALSE }
 
    $rel = Invoke-WebRequest -Headers $auth -Method POST -Body $release -Uri https://api.github.com/repos/$user/$repo/releases
    if ($null -ne $rel)
    {
        return (ConvertFrom-Json $rel.Content).id
    }
  
    $host.SetShouldExit(101)
    exit
}

function GenerateJWT(){
    $currentTime = [int][double]::parse((Get-Date -Date $((Get-Date).ToUniversalTime()) -UFormat %s))
    $expireTime = $currentTime + 300; # token is valid for 5 minutes 
    $currentTime = $currentTime - 10; # account for time drift between servers

    #github-id and github-cer need to be specified in the Jenkins environment variables on your installation
    $id = [System.Environment]::GetEnvironmentVariable('github-id')
    $cert = [System.Environment]::GetEnvironmentVariable('github-cer')

    [hashtable]$header = @{alg = "RS256"; typ = "JWT"}

    [hashtable]$payload = @{iat = $currentTime; exp = $expireTime; iss = $id }

    $headerjson = $header | ConvertTo-Json -Compress
    $payloadjson = $payload | ConvertTo-Json -Compress
        
    $headerjsonbase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($headerjson)).Split('=')[0].Replace('+', '-').Replace('/', '_')
    $payloadjsonbase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($payloadjson)).Split('=')[0].Replace('+', '-').Replace('/', '_')

    $data = $headerjsonbase64 + "." + $payloadjsonbase64

    $privatePem = Get-Content -Path "$cert" -Raw

    [System.Security.Cryptography.RSA]$rsa = New-Object System.Security.Cryptography.RSACryptoServiceProvider;
    $rsa.ImportFromPEM($privatePem)
       
    $signature = [Convert]::ToBase64String(
        $rsa.SignData(
            [System.Text.Encoding]::UTF8.GetBytes($data),
            [Security.Cryptography.HashAlgorithmName]::SHA256,
            [Security.Cryptography.RSASignaturePadding]::Pkcs1
        )
    ).Split('=')[0].Replace('+', '-').Replace('/', '_')

    $token = "$data.$signature"
    $token
}
function GetAccessToken()
{
    $token = GenerateJWT 
    $auth = @{"Authorization"="Bearer $token"}
    
    $installations = Invoke-WebRequest -Headers $auth -Method GET -Uri https://api.github.com/app/installations
    ConvertFrom-Json $installations.Content | ForEach-Object {
        $installationID = $_.id
    }

    $accessTokens = Invoke-WebRequest -Headers $auth -Method POST -Uri https://api.github.com/app/installations/$installationID/access_tokens
    ConvertFrom-Json $accessTokens.Content | ForEach-Object {
        $token = $_.token
    }
    
    $token
}

$token = GetAccessToken
$auth = @{"Authorization"="token $token"}

$releaseID = FindRelease $tag
if ($releaseID -eq 0) {
    $releaseID = CreateRelease $tag
}
Delete $releaseID $file
Upload $releaseID $file

$fileName = Split-Path $file -Leaf
return "https://github.com/$user/$repo/releases/download/$tag/$fileName"
