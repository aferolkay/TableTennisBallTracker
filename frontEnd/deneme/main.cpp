#include <QtWidgets>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QGraphicsScene scene;
    QGraphicsView view(&scene);

    // Create the ball item
    QGraphicsEllipseItem ballItem;
    ballItem.setRect(0, 0, 20, 20); // Set the position and size of the ball
    ballItem.setBrush(Qt::red); // Set the color of the ball

    // Add the ball item to the scene
    scene.addItem(&ballItem);

    view.show();

    return app.exec();
}
