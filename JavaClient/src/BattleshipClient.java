
import java.io.*;
import java.net.*;
import java.util.Scanner;

public class BattleshipClient {
    public static void main(String[] args) {
        String serverIp = "192.168.1.118"; // Replace with your server IP
        int serverPort = 6969;

        try (Socket clientSocket = new Socket(serverIp, serverPort);
             BufferedReader serverInput = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
             PrintWriter serverOutput = new PrintWriter(clientSocket.getOutputStream(), true);
             Scanner scanner = new Scanner(System.in)) {

            System.out.println("Connected to the server. Waiting for instructions...");

            // Game loop
            while (true) {
                String messageFromServer = serverInput.readLine(); // Read the message from the server
                if (messageFromServer == null) {
                    System.out.println("Server disconnected.");
                    break;
                }

                System.out.println(messageFromServer); // Print the message

                if (messageFromServer.contains("Pick an orientation") ||
                        messageFromServer.contains("Pick the starting point") ||
                        messageFromServer.contains("Pick a direction")) {

                    // Input and send ship placement details
                    System.out.print("Enter your response: ");
                    String response = scanner.nextLine();
                    serverOutput.println(response);

                } else if (messageFromServer.contains("Your turn")) {

                    // Input and send the move
                    System.out.print("Enter your move (x,y): ");
                    String move = scanner.nextLine();
                    serverOutput.println(move);

                } else if (messageFromServer.contains("win") || messageFromServer.contains("lose")) {
                    System.out.println("Game over!");
                    break;
                }
            }
        } catch (IOException e) {
            System.err.println("Connection error: " + e.getMessage());
        }
    }
}
