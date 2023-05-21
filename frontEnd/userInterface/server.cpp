#include "server.h"



Server::Server(QObject *parent) : QObject(parent)
{
    server = new QTcpServer(this);
    connect(server, &QTcpServer::newConnection, this, &Server::handleNewConnection);
}

void Server::start()
{
    //if (server->listen(QHostAddress::Any, 6000))
    if (server->listen(QHostAddress::LocalHost, 6000))
    {
        qDebug() << "Server started. Listening on port 6000...";
    }
    else
    {
        qDebug() << "Failed to start server.";
    }
}

void Server::handleNewConnection()
{
    if (clientSocket)
    {
        // Already connected, reject additional clients
        QTcpSocket *newClient = server->nextPendingConnection();
        newClient->close();
        newClient->deleteLater();
    }
    else
    {
        // Accept the new client connection
        clientSocket = server->nextPendingConnection();
        qDebug() << "Client connected.";

        connect(clientSocket, &QTcpSocket::readyRead, this, &Server::readData);
        connect(clientSocket, &QTcpSocket::disconnected, this, &Server::handleDisconnection);
    }
}

void Server::readData()
{
    QByteArray data = clientSocket->readAll();
    qDebug() << "Received data from client:" << data;
}

void Server::handleDisconnection()
{
    qDebug() << "Client disconnected.";
    clientSocket->deleteLater();
    clientSocket = nullptr;
}
