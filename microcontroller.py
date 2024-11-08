#include <stdio.h>
#include <string.h>
#include <unistd.h>     // for read and write functions
#include <fcntl.h>      // for open and O_* flags
#include <termios.h>    // for serial port settings

int main() {
    int serial_port = open("/dev/ttyUSB0", O_RDWR);  // Change to your serial port (e.g., /dev/ttyUSB0)

    // Check for errors
    if (serial_port < 0) {
        perror("Error opening serial port");
        return 1;
    }

    // Configure serial port
    struct termios tty;
    memset(&tty, 0, sizeof(tty));

    if (tcgetattr(serial_port, &tty) != 0) {
        perror("Error getting serial port attributes");
        return 1;
    }

    tty.c_cflag = B9600 | CS8 | CLOCAL | CREAD;   // Baud rate: 9600, 8-bit characters
    tty.c_iflag = IGNPAR;                         // Ignore framing errors and parity errors
    tty.c_oflag = 0;
    tty.c_lflag = 0;

    tcflush(serial_port, TCIFLUSH);
    tcsetattr(serial_port, TCSANOW, &tty);

    // Read data
    char read_buf[256];
    memset(read_buf, 0, sizeof(read_buf));

    while (1) {
        int num_bytes = read(serial_port, &read_buf, sizeof(read_buf) - 1);

        if (num_bytes < 0) {
            perror("Error reading from serial port");
            break;
        }

        read_buf[num_bytes] = '\0'; // Null-terminate the string

        // Check received command
        if (strcmp(read_buf, "CLOSE") == 0) {
            printf("Received CLOSE command\n");
            // Perform the action for CLOSE command
        } else if (strcmp(read_buf, "OPEN") == 0) {
            printf("Received OPEN command\n");
            // Perform the action for OPEN command
        } else {
            printf("Unknown command: %s\n", read_buf);
        }
    }

    close(serial_port);
    return 0;
}
