Add-Type -AssemblyName PresentationCore,PresentationFramework

$msgBody = "Please ensure this script is running in the root directory of your project"
$msgTitle = "Confirm Correct Location"
$msgButton = 'OKCancel'
$msgImage = 'Warning'
$result = [System.Windows.MessageBox]::Show($msgBody,$msgTitle,$msgButton,$msgImage)
if ($result -eq 'Cancel') {
  Exit
}

$project_root = $PWD.Path
$root_dir_only = Get-Location | Split-Path -Leaf 
$project_underscores = $root_dir_only.Replace('-', '_')
$temp_location_root = "C:\temp\temp_dagsterbase_repo"
Push-Location
if (Test-Path $temp_location_root) {
  rm -R -Force $temp_location_root
}
mkdir $temp_location_root
cd $temp_location_root
git clone git@gitlab.redchimney.com:dataengineering/data-engineering-templates/de-dagsterbase-template.git
cd .\de-dagsterbase-template\de_dagsterbase_template
# cd %PROJECT_ROOT%
$parent_dir = Get-Location | Split-Path -Leaf 
$parent_underscores = $parent_dir.Replace('-', '_')

robocopy .\de_group_resources\ "${project_root}\${project_underscores}\de_group_resources\"
robocopy .\de_group_sensors\ "${project_root}\${project_underscores}\de_group_sensors\"
robocopy ..\cicd_scripts\ "${project_root}\cicd_scripts\"

Pop-Location
