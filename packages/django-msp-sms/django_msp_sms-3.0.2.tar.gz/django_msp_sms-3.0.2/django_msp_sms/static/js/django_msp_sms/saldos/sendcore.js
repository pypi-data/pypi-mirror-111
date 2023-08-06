
function AjaxAsyncTask(args) {
    
    this.lista = args.list    
    this.porcentaje = 0
    this.deferred = $.Deferred()
    this.promise = deferred.promise()
    this.index = 0
    this.indexlist = 0
    this.$progress = args.$progress
    this.url = args.url
    this.interval = args.interval
    
    if (args.onDone == undefined) 
        this.result = function(){}    
    else
        this.result = args.onDone    

    if (args.onSuccesRequest == undefined) 
        this.onSuccesRequest = function(){}    
    else
        this.onSuccesRequest = args.onSuccesRequest

    this.failed = function() {
        $progress.css({
            'background': 'red'
        });
    }

    this.inProgress = function() {
        $progress.attr('style',' width:'+porcentaje+'%')
        $progress.text(porcentaje+'%')

    }

    this.sendData = function(){
        debugger;
        console.log(this.lista)
         if (porcentaje < 100) {
            var data = JSON.stringify(lista[indexlist])
            $.ajax({
                url:url, 
                type : 'get', 
                data: { 'data': data },
            }).done(function(data){
                onSuccesRequest(data)
                porcentaje = ((indexlist+1)*100)/lista.length
                deferred.notify()

                indexlist += 1
                sendData()
            })



        } else {
            this.deferred.resolve()
        }
    }

    this.uniqueRequest = function(){
        var data = JSON.stringify(lista)
        $.ajax({
            url:url, 
            type : 'get', 
            data: { 'data': data },
            success: onSuccesRequest ,
        })
        countUp()
    }

    this.countUp = function() {
        if (porcentaje < 100) {
            deferred.notify();
            porcentaje = ((index+1)*100)/lista.length
            index += 1
            setTimeout( function(){ 
                countUp();
            }, interval)
            
        } else {
            deferred.notify();
            this.deferred.resolve()
        }
    }

    this.promise.done(result)
    this.promise.fail(failed)
    this.promise.progress(inProgress)


    if (interval != undefined) {
        uniqueRequest()
    }
    else{
        sendData()
    }
}

function sendMessages(clientes_ids){
    var data = JSON.stringify(clientes_ids)
    var vencidos=$("vencidos").val();
    mensajes_enviados = 0;
    mensajes_no_enviados = 0;
    $.ajax({
        url:'/sms/saldos/get_mensajes_saldos/',
        type : 'get', 
        data: { 'data': data,'vencidos':vencidos, },
    }).done(function(data){
        if (data.cargos != null) {
            if (data.cargos.length > 0){
                if (data.error== null)
                {
                    AjaxAsyncTask({
                        list: data.cargos,
                        $progress: $("#progreso"),
                        url:'/sms/saldos/enviar_cargo/',
                        onSuccesRequest: function(data){
                            if(data.resultado.code == 'sms_11')
                            {mensajes_enviados = mensajes_enviados + 1}
                            else if(data.resultado.code == 'sms_19')
                            {mensajes_no_enviados = mensajes_no_enviados + 1}
                            showChanges(data, mensajes_enviados,mensajes_no_enviados)
                        },
                        onDone: function(){
                            
                            $('#progreso').text('');
                            $('#progreso').attr('style',' width:0%');
                            $("#id_clientes-deck").text("");
                            $("#id_clientes").text("");2
                            $(".yourlabs-autocomplete autocomplete-light-widget").text("");
                            $("#btnEnviar-estadosCuenta").show();
                            
                        }
                    })
                }
                else
                {
                    $('#alert').attr('class','alert alert-danger fade in');
                    var mensaje_alerta = data.error;
                    $("#alertContainer").html(mensaje_alerta);
                }
            }
            else{
                alert('No hay mensajes para ninguno de los clientes seleccionados');
                $(".yourlabs-autocomplete autocomplete-light-widget").text("");
                location.reload();
            }
        }
    })
}

function showChanges(data, mensajes_enviados,mensajes_no_enviados){
    if (data.resultado.code == 'sms_11') {
        $("#alert").show();
        $('#alert').attr('class','alert alert-info fade in');
        var mensaje_alerta = mensajes_enviados+" Mensajes Enviados correctamente.<br>"
        $("#alertContainer").html(mensaje_alerta);
        // if (data.clientes_sin_mensaje.length>0) {
        //     mensaje_alerta =mensaje_alerta +"<br><strong>Clientes sin cargos:</strong><br>"+data.clientes_sin_mensaje.join('<br/>');
        // }
        // if (data.clientes_con_telefono_invalido.length>0) {
        //     mensaje_alerta =mensaje_alerta +"<br><strong>Clientes con telefono invalido:</strong><br>"+data.clientes_con_telefono_invalido.join('<br/>');
        // }
        
    }
    else if(data.resultado.code == 'sms_19')
    {   $("#alert2").removeClass('hidden');
        $("#alert2").show();
        $('#alert2').attr('class','alert alert-warning fade in');
        var mensaje_alerta = mensajes_no_enviados+" Mensajes no Enviados, por ser numeros fijos o no existir.<br>"
        $("#alertContainer2").html(mensaje_alerta+' <a href='+data.media_url+data.carpeta+data.nom_archivo+' title="'+data.nom_archivo+'" id="archivo" download="'+data.nom_archivo+'">Descargar lista</a></strong><br>');
        
    }
    /*alert("Mensajes Enviados");*/

}