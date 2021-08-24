 <?php
session_start();

if(isset($_POST['submit_pass']) && $_POST['pass'])
{
 $pass=$_POST['pass'];
 if($pass=="seafoam")
 {
  $_SESSION['password']=$pass;
 }
 else
 {
  $error="Incorrect Password";
 }
}

if(isset($_POST['page_logout']))
{
 unset($_SESSION['password']);
}
?>

<?php
if($_SESSION['password']=="seafoam")
{
 ?>
 <p><a href="formcode.html"> proceed to form </a></p>
 <?php
}
else
{
 ?>
 <h1> ERROR </h1>
 <?php	
}
?>

</div>
</body>
</html>