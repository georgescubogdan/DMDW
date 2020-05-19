using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.SignalR;


namespace DMDW.Hubs
{
    public class TestHub : Hub
    {
        public static string response;
        public async Task SendMessage(string user, string message)
        {
            response = message;
            //await Clients.All.SendAsync("ReceiveMessage", user, message);
        }
    }

}
