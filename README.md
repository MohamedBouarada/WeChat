# WeChat

<h1> <img src = "https://github.com/Harpia-Vieillot/Harpia-Vieillot/blob/main/resources/analytics.webp" width="7%"> Table of Contents </h1>

  <ol>
    <li><a href="#">About</a></li>
    <li><a href="#">What we Learnt ?</a></li>
    <li> <a href="#">Features</a></li>
    <li><a href="#">Project structure</a></li>
    <li><a href="#">Dependencies</a></li>
    <li><a href="#">Setup</a></li>
    <li><a href="#">Demo</a></li>
  </ol>
  

<h1> <img src = "https://github.com/Harpia-Vieillot/Harpia-Vieillot/blob/main/resources/analytics.webp" width="7%"> About </h1>

A chatroom application written in python , that is based on RabbitMQ using LDAP for authentication and RSA encryption



<h1> <img src = "https://github.com/Harpia-Vieillot/Harpia-Vieillot/blob/main/resources/analytics.webp" width="7%"> What we Learnt ? </h1>

- **Objective 1**: LDAP server configuration, managing user authentication.
- **Objective 2**: How to set up a certificate authority server that accepts certification requests, creates them, then signs them in order to verify their state
- **Objective 3**: How to use RabbitMQ for chatting.
- **Objective 4**: How to use RSA encryption/decryption for secure communication

<h1> <img src = "https://github.com/Harpia-Vieillot/Harpia-Vieillot/blob/main/resources/analytics.webp" width="7%"> Features </h1>

1- **Client side :**
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Register -> Enter credentials To create an account
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Login 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. View all connected users
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Select a chat room
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. View all users in that room
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Using RSA technique  to encrypt/decrypt all messages sent between clients.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Quit the application

2- **Server side :**
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Add new user to the active directory via LDAP 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Get a x509 certificaton via certificate authority server 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. On login,verify user in the active directory via LDAP
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Verify the Certificate signature via authority server
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Start communication with RabbitMQ server
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Encrypt /decrypt messages while exchanging them between users

<h1> <img src = "https://github.com/Harpia-Vieillot/Harpia-Vieillot/blob/main/resources/analytics.webp" width="7%"> Project structure </h1>

```bash
 WeChat/
   └── certificate_authority/
     ├── ...
     ├── ca_server.py
     ├── ...
   ├── ...
   ├── controller.py
   ├── home.py
   ├── welcome.py
   ├── client_interface.py
   ├── ...
```

<h1> <img src = "https://github.com/Harpia-Vieillot/Harpia-Vieillot/blob/main/resources/analytics.webp" width="7%"> Dependencies </h1>

- [RabbitMQ](https://www.rabbitmq.com/): Messaging Broker based on AMQP protocol.
- [pycryptodome](https://pypi.org/project/pycryptodome/): A python library for encryption/decryption.
- [Tkinter](https://docs.python.org/3/library/tkinter.html): Tkinter is the de facto way in Python to create Graphical User interfaces (GUIs) and is included in all standard Python Distributions.
- [cryptography](https://cryptography.io/en/latest/): python library for X509 certs.
- [OpenLDAP](https://www.openldap.org/): is an open-source implementation for LDAP protocol
- [LAM](https://www.ldap-account-manager.org/lamcms/): LDAP Account Manager (LAM) is a webfrontend for managing entries stored in an LDAP directory
- [Pika](https://pika.readthedocs.io/en/stable/): Rabbitmq python client

<h1> <img src = "https://github.com/Harpia-Vieillot/Harpia-Vieillot/blob/main/resources/analytics.webp" width="7%"> Setup </h1>

### 1. Open LDAP server in your machine
### 2. Run rabbitMQ service
### 3. Clone the `WeChat` repository locally
### 4. Install dependencies
### 5. Add `.env` file that contains:
        - CA_SELF_CERT (the path to the self signed certificate of the certificate authority)
        - CA_PRIVATE_KEY (the path to the certificate authority private key)
        - CA_CLIENT_CERT_DIR (the path to the directory which will contain the clients' certificates)
        - CA_CLIENT_KEY_DIR (the path to the directory which will contain the clients' private keys)
        - CA_CLIENT_CSR_DIR (the path to the directory which will contain the clients' certificate requests)
        
### 6. Create an Instance of Authority-server

```bash
$ python3 ./certificate_authority/ca_server.py
```

### 7. Create an Instance of Messaging controller

```bash
$ python3 ./controller.py
```

### 8. Run

```bash
$ python3 ./home.py
```

<h1> <img src = "https://github.com/Harpia-Vieillot/Harpia-Vieillot/blob/main/resources/analytics.webp" width="7%"> Demo </h1>

[![Demo Video]()](https://www.youtube.com/watch?v=mZdrY4Zo8A4)












