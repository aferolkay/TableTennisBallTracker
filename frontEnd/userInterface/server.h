
#ifndef SERVER_H
#define SERVER_H

#include <QtNetwork>
#include <QObject>

class Server : public QObject
{
    Q_OBJECT

public:
    explicit Server(QObject *parent = nullptr);

    void start();

private slots:
    void handleNewConnection();

    void readData();

    void handleDisconnection();

private:
    QTcpServer *server = nullptr;
    QTcpSocket *clientSocket = nullptr;
};

#endif // SERVER_H
