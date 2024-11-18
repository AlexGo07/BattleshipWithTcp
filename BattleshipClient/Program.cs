using System;
using System.IO;
using System.Net.Sockets;

class BattleshipClient
{
    static void Main(string[] args)
    {
        string serverIp = "192.168.214.14";
        int serverPort = 6969;

        try
        {
            using (TcpClient client = new TcpClient(serverIp, serverPort))
            using (NetworkStream stream = client.GetStream())
            using (StreamReader reader = new StreamReader(stream))
            using (StreamWriter writer = new StreamWriter(stream) { AutoFlush = true })
            {
                Console.WriteLine("Connected to the server. Waiting for instructions...");

                while (true)
                {
                    string message = reader.ReadLine();
                    if (message == null)
                    {
                        Console.WriteLine("Connection closed by server.");
                        break;
                    }

                    Console.WriteLine(message);

                    if (message.Contains("Pick an orientation") ||
                        message.Contains("Pick the starting point") ||
                        message.Contains("Pick a direction"))
                    {
                        // Input and send the ship placement details
                        string response = Console.ReadLine();
                        writer.WriteLine(response);
                    }
                    else if (message.Contains("Your turn"))
                    {
                        // Input and send the move
                        Console.Write("Enter your move (x,y): ");
                        string move = Console.ReadLine();
                        writer.WriteLine(move);
                    }
                    else if (message.Contains("win") || message.Contains("lose"))
                    {
                        Console.WriteLine("Game over!");
                        break;
                    }
                }
            }
        }
        catch (Exception e)
        {
            Console.WriteLine("An error occurred: " + e.Message);
        }
    }
}
