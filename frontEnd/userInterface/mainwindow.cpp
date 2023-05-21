#include "server.h"
#include "mainwindow.h"
#include "ui_mainwindow.h"

QList<QLabel *> ballList;


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    placeBall(20,20);
    placeBall(20,40);
    Server server;
    server.start();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::placeBall(int x, int y){
    x = ui->table->x() + x*2;
    y = ui->table->y() + y*2;
    QLabel *label = new QLabel(this);
    ballList.append(label);
    label->setText("<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">"+QString::number(ballList.length())+"</span></p></body></html>");
    //Here is how to change position:
    label->setGeometry(x,y,21,21);
    label->setStyleSheet("background-color: rgb(255, 148, 98); border-radius: 10px");
}

void MainWindow::clearBall(){
    for(int i=0 ; i<ballList.length() ; i++)
        delete ballList[i];
    ballList.clear();
}


void MainWindow::on_pushButton_clicked()
{
    clearBall();
}

