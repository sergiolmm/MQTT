var mqtt;
var reconnectTimeout = 2000;
var host="91.121.93.94";//test.mosquitto.org";
var port=8080; // quando usando webSocket usar essa porta ver docs.
// var port=8081; quando https
var estado = false;

function msg(){  
    alert("Hello Javatpoint");  
   }  

function onConnect(){
    console.log("Conectado");
    const userText = document.getElementById("statusConexao");
    //userText.textContent = "Conectado a :" +host + " na porta :" +port;
    // aqui escolhe para quem vai assinar para recebe coisas...
   // mqtt.subscribe("hello");
    userText.textContent = "Conectado a :" +host + " na porta :" +port + 
    " em hello"   ;
}

function onFailure(){
    console.log("Falha");
    const userText = document.getElementById("statusConexao");
    userText.textContent = "Falha ao conectar tente novamente";        
}

function onMessageArrived(msg ){
    console.log("Mensagem chegando :");            
    console.log(msg.payloadString);            
    //const userText2 = document.getElementById("mensagens");
    //var msgOld = userText2.value;    
    //userText2.textContent = "Payload :" + msg.payloadString + "\n" + msgOld ;
}

function connect(){
    console.log("Iniciando mqtt");
   // if (location.protocol == 'https:') {
   //port = 8081;
   // }
    var clientId  = "mqtt_p_js_" + parseInt(Math.random() * 100000, 10);
    mqtt = new Paho.MQTT.Client(host,port, clientId);
    var options ={
        timeout :3,
        onSuccess: onConnect,  
       // useSSL: true,  
        onFailure: onFailure,
    };
    mqtt.onMessageArrived = onMessageArrived
    mqtt.connect(options);
}

function mandaComando(msg){       
    console.log(msg);
    message = new Paho.MQTT.Message(msg);
    // aqui escolhe para quem vai publicar
    message.destinationName = "hello";

    mqtt.send(message);


    

}

function publicar(){
    
    mandaComando('{ "cmd" : "3"}');
}



function trocar(){    
    btn = document.getElementById("btn");
    if (!estado){        
        btn.src = "red_btn.png";
        mandaComando('{ "cmd" : "on"}');
    }else{
        btn.src = "green_btn.png";
        mandaComando('{ "cmd" : "off"}');

    }
    estado = !estado;
}


function chave(){    
    if (document.getElementById("on").checked){
       // alert("on");
        mandaComando('{ "cmd" : "on")}');
    }
    if (document.getElementById("off").checked){
       // alert("off");
        mandaComando('{ "cmd" : "on")}');
    }
}