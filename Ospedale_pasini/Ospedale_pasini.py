# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 18:18:49 2021

@author: marsi
"""

import http.server
import sys,signal
import socketserver
import threading

#manage the wait witout busy waiting
waiting_refresh = threading.Event()

# primi articoli di ogni testata
first_articles = [] 


# Legge il numero della porta dalla riga di comando
if sys.argv[1:]:
  port = int(sys.argv[1])
else: #porta di default, nel caso non venga specificato nella linea di comando
  port = 8080
  
  # classe che mantiene le funzioni di SimpleHTTPRequestHandler e implementa
# il metodo get nel caso in cui si voglia fare un refresh
class ServerHandler(http.server.SimpleHTTPRequestHandler):        
    def do_GET(self):
        # Scrivo sul file AllRequestsGET le richieste dei client     
        with open("AllRequestsGET.txt", "a") as out:
          info = "GET request,\nPath: " + str(self.path) + "\nHeaders:\n" + str(self.headers) + "\n"
          out.write(str(info))
        if self.path == '/refresh':
            resfresh_contents()
            self.path = '/'
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        
# ThreadingTCPServer per gestire più richieste
server = socketserver.ThreadingTCPServer(('127.0.0.1',port), ServerHandler)

#-----------
# la parte iniziale è identica per tutti i giornali
header_html = """
<html>
    <head>
        <style>
            h1 {
                text-align: center;
                margin: 0;
            }
            h2 {
                text-align: center;
                margin: 0;
                font-family: arial;
            }
            table {width:70%;}
            img {
                max-width:300;
                max-height:200px;
                width:auto;
            }
            td {width: 33%;}
            p {text-align:justify;}
            td {
                padding: 20px;
                text-align: center;
            }
            .topnav {
  		        overflow: hidden;
  		        background-color: CC0033;
  		    }
            .topnav a {
  		        float: left;
  		        color: white;
  		        text-align: center;
  		        padding: 14px 16px;
  		        text-decoration: none;
  		        font-size: 17px;
  		    }        
  		    .topnav a:hover {
  		        background-color: #ddd;
  		        color: black;
  		    }        
  		    .topnav a.active {
  		        background-color: 990033;
  		        color: white;
  		    }
        </style>
    </head>
    <body>
        <title>Pasini's ASL</title>
"""

# la barra di navigazione è identica per tutti i giornali
navigation_bar = """
        <br>
        <br>
        <br>
        <div class="topnav">
            <a class="active" href="http://127.0.0.1:{port}">Home</a>
            <a href="http://127.0.0.1:{port}/pronto_soccorso.html">Pronto Soccorso</a>
            <a href="http://127.0.0.1:{port}/fascicolo_sanitario.html">Fascicolo sanitario</a>
            <a href="http://127.0.0.1:{port}/vaccino.html">Vaccino COVID-19</a>
            <a href="http://127.0.0.1:{port}/green_pass.html">Green Pass</a>
  		    <a href="http://127.0.0.1:{port}/refresh" style="float: right">Aggiorna contenuti</a>
            <a href="http://127.0.0.1:{port}/Informazioni pazienti ospedale.pdf" download="Informazioni pazienti ospedale.pdf" style="float: right">Download Informazioni utili  pdf</a>
            <a href="http://127.0.0.1:{port}/CupWeb.html">CupWeb</a>

  		</div>
        <br><br>
        <table align="center">
""".format(port=port)


footer_html = """
        </table>
    </body>
</html>
"""


#la parte finale per la pagina pronto soccorso
end_page_green_pass= """
        <br><br>
		<form action="http://127.0.0.1:{port}/green_pass" method="post" style="text-align: center;">
		  <img src='images/green pass.png'/ width="100" height="100"align="right">
          <h1><strong>Come Ricevere il green pass</strong></h1><br>
          <p>Dal 1 luglio 2021 la Certificazione verde COVID-19 e' valida come EU digital COVID certificate.<br>
           Deve essere ottenuta esclusivamente attraverso i seguenti canali ufficiali, che prevedono l'acquisizione di identita' digitale. <br>
           ATS ha inviato al Ministero della Salute tutti i dati relativi alla guarigione dei propri assistiti,<br>
           che dovrebbero aver ricevuto codice (AUTHCODE) NCUG utile a scaricare il proprio green pass attraverso il sito: </p>
              <a href=" https://www.dgc.gov.it/web/"><p>Certificazione verde COVID-19</p></a><br><br>
              

            Se non ha ricevuto alcun codice e' comunque possibile ottenere la Certificazione verde COVID-19 digitalmente tramite:  <br>

            Via APP attraverso:<br>
                -IMMUNI<br>
                -APP IO<br>
            In alternativa, e' possibile recarsi dal proprio medico di base o andare in farmacia fornendo il proprio Codice Fiscale e Tessera Sanitaria. <br>
            Per ogni ulteriore informazione visitare il sito:<br>
         
          <a href=" https://www.dgc.gov.it/web/faq.html"><p>Per maggiori informazioni clicca qui</p></a>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

end_page_ps= """
        <br><br>
		<form action="http://127.0.0.1:{port}/pronto_soccorso" method="post" style="text-align: center;">
        		  <img src='images/ps.png'/ width="100" height="100">

    		 <h1>Come funziona il pronto soccorso: il triage e i codici</h1>
             Lo scopo del triage e' proprio quello di valutare la gravita' della patologia della persona arrivata al pronto soccorso e assegnargli un codice, che consentira' ai medici di prestare le cure in modo efficace e di procedere con il ricovero ospedaliero quando e se necessario.

            <h2>La priorita' dell'intervento viene indicata, come e' noto, con una gamma di colori:</h2>

            <h2>Codice bianco pronto soccorso</h2> - Viene assegnato a pazienti che hanno sintomi e patologie di lieve entita'. Si tratta di persone che potrebbero essere curate dal medico di base, per questo chi ha questo codice al pronto soccorso spesso attende molto tempo prima di essere visitato.
            <h2>Codice azzurro pronto soccorso</h2> - Si tratta di un codice che non e' molto comune ed e' leggermente piu' grave di quello bianco. Indica pazienti che non hanno bisogno di cure immediate e per questo possono aspettare. Sia il codice bianco che quello azzurro sono soggetti al pagamento del ticket.
            <h2>Codice verde pronto soccorso</h2> - Questo colore identifica i pazienti che presentano patologie che non sono critiche e una condizione di salute stabile. La persona ha bisogno di ricevere un intervento da parte dei medici, ma la sua priorita' e' secondaria rispetto al codice giallo e a quello rosso.
            <h2>Codice giallo pronto soccorso</h2> - Indica pazienti che hanno condizioni vitali stabili, ma rischiano di aggravarsi. Viene assegnato a pazienti che hanno difficolta' respiratorie, sono intossicati, ad esempio per l'ingestione di funghi, presentano stati di coscienza alterata e sono feriti in modo piu' o meno grave.
            <h2>Codice rosso pronto soccorso</h2> - Questo codice indica un caso grave che ha la priorita' assoluta rispetto agli altri pazienti poiche' la persona arrivata al pronto soccorso e' in pericolo di vita e ha bisogno di ricevere cure d'urgenza.
            <a href=" https://www.auslromagna.it/organizzazione/dipartimenti/emergenza/ps-forli"><p>Pronto soccorso di forli'</p></a>
        </form>
		<br>
    </body>
</html>
""".format(port=port)

end_page_fs= """
        <br><br>
		<form action="http://127.0.0.1:{port}/fascicolo_sanitario" method="post" style="text-align: center;">
             <h1> Come utilizzare e ottenere il Fascicolo Sanitario Elettronico</h1>
             <img src='images/fs.png'/ width="100" height="100">
    		 <p>L'utilizzo del Fascicolo Sanitario e degli altri servizi online - per quanto intuitivo e guidato - puo'' richiedere qualche consiglio, soprattutto nelle prime sessioni e per l'uso delle funzioni più complesse.<br>
             Per questo, ti abbiamo messo a disposizione piu' strumenti di aiuto:<br>
              <a href=" https://support.fascicolo-sanitario.it/guida/informazioni-utili/le-guide-e-l%26%2339%3Bassistenza/la-guida-online"><p>-la guida online<br></p></a>
              un sistema di help contestuale nato per spiegarti come gestire i diversi elementi dell'interfaccia del Fascicolo
              
              <a href=" https://support.fascicolo-sanitario.it/guida/informazioni-utili/le-guide-e-l%26%2339%3Bassistenza/la-guida-online"><p>-le FAQ<br></p></a>
              una raccolta classificata per aree delle piu' frequenti domande a carattere generale rivolte dagli utenti agli operatori del servizio di assistenza, e delle relative risposte<br>
             -questa Guida<br>
              un vero e proprio manuale d'uso del FSE e degli altri Servizi Sanitari online<br><br>
              Se si vuole accedere al proprio fascicolo elettronico basta clicccare su "accedi" in nella barra di navigazione in alto e inserire le rispettive credenziali</p>          
		</form>
		<br>
    </body>
</html>
""".format(port=port)

end_page_CupWeb= """
        <br><br>
        <img src='images/cup.png'/ width="100" height="100"align="right">

		<form action="http://127.0.0.1:{port}/pronto_soccorso" method="post" style="text-align: center;">
		 <h1>Prenotazioni online di visite ed esami specialistici</h1><br><br>
 
<h2>CUPWeb è il sistema di prenotazione e disdetta online delle prestazioni specialistiche della Regione Emilia-Romagna.
Ad oggi è possibile prenotare le visite e gli esami maggiormente richiesti per il Servizio Sanitario Regionale e per la Libera Professione.<br>

SENZA AUTENTICAZIONE PUOI:</h2><br>

<p>disdire gli appuntamenti prenotati tramite CUPWeb, sportello CUP/farmacia o Numero Verde
pagare gli appuntamenti prenotati<br>
<h2>SE TI AUTENTICHI PUOI ANCHE:<h2><br>

prenotare una o più impegnative in SSN e libera professione<br>
modificare uno o più appuntamenti prenotati tramite CUPWeb, sportello CUP/farmacia o Numero Verde<br>
visualizzare le prenotazioni sino alla data fissata<br>
ristampare il promemoria dell'appuntamento e dell'eventuale costo della prestazione prenotata.<br>
<a href="https://support.fascicolo-sanitario.it/guida/accedi-al-tuo-fse"><p>Per maggiori informazioni sulle modalità di accesso<br></p></a>


		</form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina della prenotazione del vaccino per il covid-19
end_page_vaccino= """
        <br><br>
		<form action="http://127.0.0.1:{port}/vaccino" method="post" style="text-align: center;">
		  <img src='images/vaccino.png'/ width="100" height="100">
          <h1><strong>COME SI PRENOTA?</strong></h1><br>
            <p>Tutti gli aventi diritto si possono prenotare, senza prescrizione medica, scegliendo tra queste modalita'':<br>
            -Agli sportelli Cup dell'Ausl ( Centri Unici Prenotazione) presenti su tutto il territorio romagnolo<br>
            -Nelle farmacie tramite il servizio Farmacup<br>
            -Telefonando al Cuptel al numero 800002255<br>
            -Online attraverso: il Fascicolo Sanitario Elettronico, l'App ER Salute<br>
            -Oppure dal proprio medico di Medicina Generale, che accogliera' le richieste e provvedera' ad organizzare le sedute vaccinali</p><br>
            <h2> Perche' vaccinarsi?</h2><br>
            <p> Il coronavirus e' molto contagioso. Anche se la maggioranza delle persone infette sviluppa soltanto sintomi lievi o e' del tutto asintomatica, una parte degli ammalati, specialmente le persone particolarmente a rischio, presenta un decorso grave.<br>
            Un sesto dei pazienti ricoverati in ospedale richiede cure intense.<br>
            Una persona contagiata dal coronavirus su 100 muore.<br>
            A partire dai 65 anni, il rischio di essere ricoverati in ospedale per coronavirus aumenta del 10-20 per cento. A partire dai 70 anni, il rischio morire di coronavirus aumenta del 3-14 per cento.<br>
            La vaccinazione diminuisce il rischio di contrarre il coronavirus e di trasmetterlo; in questo modo potete proteggere le persone particolarmente a rischio nella vostra famiglia, nella vostra economia domestica o nel vostro ambiente di lavoro. Più persone sono vaccinate, meno il virus circola nella società e meno persone si ammalano o muoiono di coronavirus.<br>            
            La vaccinazione protegge contro la malattia da nuovo coronavirus e contro la sua trasmissione<br>
            La vaccinazione anti-COVID-19 protegge dal coronavirus. Attualmente e' la migliore strategia – insieme alle regole di igiene e di comportamento – per contenere il coronavirus e ridurre il numero di decorsi gravi e di decessi in Svizzera.<br>
            Dati attuali indicano che la trasmissione del coronavirus ad altre persone e' ridotta dopo una vaccinazione completa. Tuttavia, la vaccinazione non protegge al 100 per cento dal contagio. Per questo motivo, per contenere la diffusione del coronavirus resta comunque importante che anche le persone vaccinate si attengano alle principali regole di igiene e di comportamento.<br></p>
             <a href="https://vaccinocovid.regione.emilia-romagna.it/come-prenotare"><p>Per prenotare il vaccino</p></a>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina home
end_page_index = """
        <br><br>
		<form action="http://127.0.0.1:{port}/home" method="post" style="text-align: center;">
		  <img src='images/ausl.png'/ width="100" height="100">
          <img src='images/logo.png'/ width="100" height="100" align="right">
		  <h1><strong>AZIENDA SANITARIA PASINI</strong></h1><br>
          <h2>Le ASL sono organizzate in vari dipartimenti, servizi sanitari territoriali</h2><br>
          <h2>e presidi ospedalieri e possono comprendere diversi servizi:</h2><br>
            <p style="text-align: center;">-Consultorio<br>
            -Dipartimento di prevenzione<br>
            -Servizio di comunita' assistenziale<br>
            -Servizio per le dipendenze patologiche<br>
            -Ambulatori per esami specialistici<br>
            -Assistenza domiciliare e per residenze socio-sanitarie<br>
            -Servizi per la salute mentale<br>
            -Servizi per prestazioni CUP<br>
            -Medici di famiglia convenzionati<br>
            -Pediatri<br>
            -Sert</p>
            <h2>Per poter accedere a determinati servizi e' necessario presentare una richiesta compilata dal medico di base o da uno specialista e autorizzata dalla ASL di riferimento.</h2><br>
		</form>
		<br>
    </body>
</html>
""".format(port=port)


  
# creo tutti i file utili per navigare.
def resfresh_contents():
    print("updating all contents")
    create_page_green_pass()
    create_index_page()
    create_page_prenotazione_vaccino()
    create_page_pronto_soccorso()
    create_page_fascicolo_sanitario()
    print("finished update")
    
# creazione della pagina specifica per prenotare il vaccino
def create_page_prenotazione_vaccino():
    create_page_servizio("<h1>Prenotazione vaccino</h1>"  , 'vaccino.html', end_page_vaccino )
    
# creazione della pagina specifica del FSE
def create_page_green_pass():
    create_page_servizio("<h1>Informazioni green pass</h1>", 'green_pass.html', end_page_green_pass )
    
# creazione della pagina index.html (iniziale)
# contenente pagina principale del Azienda ospedaliera
def create_index_page():
    create_page_servizio("<h1>Elaborato Pasini</h1>", 'index.html', end_page_index )
    
def create_page_pronto_soccorso():
    create_page_servizio("<h1>Pronto soccorso</h1>",'pronto_soccorso.html',end_page_ps)
    
def create_page_fascicolo_sanitario():
    create_page_servizio("<h1>Fascicolo Sanitario</h1>",'fascicolo_sanitario.html',end_page_fs)
    
def create_page_fascicolo_sanitario():
    create_page_servizio("<h1>CupWeb</h1>",'CupWeb.html',end_page_CupWeb)
    
""" 
    # creazione della pagina index.html (iniziale)
# contenente i primi articoli di ogni testata giornalistica
def create_index_page():
    f = open('index.html','w', encoding="utf-8")
    try:
        message = header_html + "<h1>Pasini's ASL</h1>" + navigation_bar
        message = message + '<tr><th colspan="2"><h2>Cronaca</h2></th>'
        message = message + '<th><h2>Tecnologia</h2></th></tr>'
        message = message + '<tr>' + first_articles[0] + first_articles[1]
        message = message + first_articles[4] + "</tr>"
        message = message + '<tr>' + first_articles[2] + first_articles[3]
        message = message + first_articles[5] + "</tr>"
        message = message + footer_html
    except:
        pass
    f.write(message)
    f.close()
"""



#metodo lanciato per la creazione delle pagine servizi
def create_page_servizio(title,file_html, end_page):
    f = open(file_html,'w', encoding="utf-8")
    try:
        message = header_html + title + navigation_bar + end_page
        message = message + footer_html
    except:
        pass
    f.write(message)
    f.close()
    



   
# lancio un thread che inizialmente carina il meteo per la città di rimini
# questo thread ogni 300 secondi (5 minuti) aggiorna il meteo e i relativi
# contenuti delle pagine     
def launch_thread_resfresh():
    t_refresh = threading.Thread(target=resfresh_contents())
    t_refresh.daemon = True
    t_refresh.start()
    
# definiamo una funzione per permetterci di uscire dal processo tramite Ctrl-C
def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if(server):
        server.server_close()
    finally:
      # fermo il thread del refresh senza busy waiting
      waiting_refresh.set()
      sys.exit(0)
      
# metodo che viene chiamato al "lancio" del server
def main():
    # lancio un thread che carica il meteo e aggiorna ricorrentemente i contenuti
    user=input ("Inserire l'username: ")
    password=input("Inserire la password: ")
    if user=='user'and password=='password':  
        launch_thread_resfresh()
        #Assicura che da tastiera usando la combinazione
        #di tasti Ctrl-C termini in modo pulito tutti i thread generati
        server.daemon_threads = True 
        #il Server acconsente al riutilizzo del socket anche se ancora non è stato
        #rilasciato quello precedente, andandolo a sovrascrivere
        server.allow_reuse_address = True  
        #interrompe l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
        signal.signal(signal.SIGINT, signal_handler)
        # cancella i dati get ogni volta che il server viene attivato
        f = open('AllRequestsGET.txt','w', encoding="utf-8")
        f.close()
    else:
            print("accesso negato")
            
        # entra nel loop infinito
    try:
        while True:
            server.serve_forever()
    except KeyboardInterrupt:
            pass
            server.server_close()

if __name__ == "__main__":
    main()

