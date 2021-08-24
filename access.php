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
 <h1>password</h1>
 <form method="post" action="" id="logout_form">
  <input type="submit" name="page_logout" value="LOGOUT">
 </form>
 <?php
}
else
{
 ?>
 <form method="post" action="" id="login_form">
  <h1>LOGIN TO PROCEED</h1>
  <input type="password" name="pass" placeholder="*******">
  <input type="submit" name="submit_pass" value="DO SUBMIT">
  <p>"Password : seafoam"</p>
  <p><font style="color:red;"><?php echo $error;?></font></p>
 </form>
 <?php	
}
?>

</div>
</body>
</html>