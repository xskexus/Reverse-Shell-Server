using System;
using System.Net;
using System.Net.Sockets;
static void main()
{
    // setting server port and ip to connect to
    Int32 port = 22443;
    String server = "127.0.0.1";
    // creating the connection
    TcpClient client = new TcpClient(server, port);
    // sending hostname to the server
    string host = "hostname " + Dns.GetHostName();
    Byte[] data = System.Text.Encoding.ASCII.GetBytes(host);
    NetworkStream stream = client.GetStream();
    stream.Write(data, 0, data.Length);
    // setting the variable to receive data
    data = new Byte[256];

    // String to store the response ASCII representation.
    String responseData = String.Empty;

    // Read the first batch of the TcpServer response bytes.
    while (true)
    {
        Int32 bytes = stream.Read(data, 0, data.Length);
        responseData = System.Text.Encoding.ASCII.GetString(data, 0, bytes);
    }
}