<?php
require 'vendor/autoload.php';

use OpenCloud\Rackspace;
$client = new Rackspace(Rackspace::US_IDENTITY_ENDPOINT, array(
    'username' => '',
    'apiKey'   => ''
));

$service = $client->computeService('cloudServersOpenStack', 'ORD');
$compute = $client->computeService('cloudServersOpenStack', 'ORD');
$server = $compute->server();
$flavors=$compute->flavorList();
$images = $compute->imageList();
$server->addFile('/root/.ssh/authorized_keys2', 'INSERT-SSH-KEY-HERE'); 


// would convert this to form for customer use

echo "How many servers: ";
$temp = fopen ("php://stdin","r");
$servNum = fgets($temp);

// check for server number
while($servNum > 3||$servNum <= 0)
	{
	echo "Server number must be between 1 and 3\n";
        echo "How many servers: ";
        $temp = fopen ("php://stdin","r");
	$servNum = fgets($temp);
	}


echo "What is the server name: ";
$temp2 = fopen ("php://stdin","r");
$servName = fgets($temp2);


// we must wait for it to complete before the IP is set
use OpenCloud\Compute\Constants\ServerState;



// flavor time
while ($flavor = $flavors->next()) {
	if (strpos($flavor->name, '1GB') !== false) {
		$oneGb = $flavor;
		break;
	}
}

// we want to use CentOS as the image
while ($image = $images->next()) {
   if (strpos($image->name, 'CentOS') !== false) {
	$centos = $image;
        break;
   }

}

// build 1-3 servers
for ($num=1; $num<=$servNum; $num++)
  {

// create server with image id. Check for errors
try {
    $response = $server->create(array(
	'name'	=> "$servName$num",
	'image' => $centos, 
        'flavor' => $oneGb,
	)
     );
}


catch (\Guzzle\Http\Exception\BadResponseException $e) {

	$responseBody = (string) $e->getResponse() ->getBody();
	$statusCode   = $e->getResponse()->getStatusCode();
	$headers      = $e->getResponse()->getHeaderLines();
    	
	echo sprintf("Status: %s\nBody: %s\nHeaders: %s", $statusCode, $responseBody, implode(', ', $headers));


}

$callback = function($server) {
    if (!empty($server->error)) {
        var_dump($server->error);
        exit;
    } else {
        echo sprintf(
            "Waiting on %s/%-12s %4s%%\n",
            $server->name(),
            $server->status(),
            isset($server->progress) ? $server->progress : 0
        );
    }
};

$server->waitFor(ServerState::ACTIVE, 600, $callback);
// set variables here for when server id and ip are available
$serverID=$server->id;
$addr = $compute->server("$serverID");
// send out server name, admin pass, and IP
echo "<html>\n";
echo "<body>\n"; 
echo "<br>\n";
echo "\n**********************\n";
echo "<br>\n";
echo "ServerName: $server->name\n<br>\n";
echo "AdminPass: $server->adminPass\n<br>\n";
echo "IP Address: $addr->accessIPv4\n<br>\n";
echo "\n**********************\n\n";
echo '</html>';
echo '</body>';

}

?>
