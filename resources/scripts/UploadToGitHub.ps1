#Requires -Version 7.0

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

$token = [System.Environment]::GetEnvironmentVariable('GITHUB_ACCESS_TOKEN')
$auth = @{"Authorization"="Bearer $token"}

$releaseID = FindRelease $tag
if ($releaseID -eq 0) {
    $releaseID = CreateRelease $tag
}
Delete $releaseID $file
Upload $releaseID $file

$fileName = Split-Path $file -Leaf
return "https://github.com/$user/$repo/releases/download/$tag/$fileName"
