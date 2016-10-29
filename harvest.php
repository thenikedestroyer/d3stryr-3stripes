
    <?php
     $siteKey = '6Le4AQgUAAAAAABhHEq7RWQNJwGR_M-6Jni9tgtA';
     $lang = 'en';
    ?>
     <?php if (isset($_POST['g-recaptcha-response'])): ?>
    <html>
     <head>
       <title>adidas Official Website | adidas</title>
     </head>
     <body>
     <?php $token=$_POST['g-recaptcha-response']; ?>
         <p id="token" value="<?php echo $token; ?>" style="padding: 3px; word-break: break-all; word-wrap: break-word;"><?php echo $token; ?></p>
     <?php else: ?>
    <html>
     <head>
       <title>d3stryr 3stripes Manual Token Harvesting | adidas</title>
            <style type="text/css">
                body {
                    margin: 1em 5em 0 5em;
                    font-family: sans-serif;
                }
                fieldset {
                    display: inline;
                    padding: 1em;
                }
            </style>
     </head>
     <body>
        <p>Token Harvesting</p>
        <form action="/harvest.php" method="post">
            <fieldset>
                <div class="g-recaptcha" data-sitekey="<?php echo $siteKey; ?>"></div>
                <script type="text/javascript" src="https://www.google.com/recaptcha/api.js">
                </script>
                <p><input type="submit" value="Submit" id="submit"/></p>
            </fieldset>
        </form>
     <?php endif; ?>
     </body>
    </html>