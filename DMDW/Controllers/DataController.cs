using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using DMDW.Hubs;
using HtmlAgilityPack;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SignalR;

namespace DMDW.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class DataController : ControllerBase
    {
        private readonly IHubContext<TestHub> _hubContext;
        public DataController(IHubContext<TestHub> hubContext)
        {
            _hubContext = hubContext;
        }
        // GET: api/Data
        [HttpGet]
        public ActionResult<string> Get()
        {
            return Ok(TestHub.response);
        }

        // GET: api/Data/5
        [HttpGet("{id}", Name = "Get")]
        public string Get(int id)
        {
            return "value";
        }

        // POST: api/Data
        [HttpPost]
        public ActionResult<string> Post([FromBody] string value)
        {
            var r = RemoveUnwantedTags(value);
            _hubContext.Clients.All.SendAsync("data", r);
            return Ok();
        }

        // PUT: api/Data/5
        [HttpPut("{id}")]
        public void Put(int id, [FromBody] string value)
        {
        }

        // DELETE: api/ApiWithActions/5
        [HttpDelete("{id}")]
        public void Delete(int id)
        {
        }

        internal static string RemoveUnwantedTags(string url)
        {
            if (string.IsNullOrEmpty(url)) return string.Empty;
            //if (string.IsNullOrEmpty(data)) return string.Empty;

            //var document = new HtmlDocument();
            //document.LoadHtml(data);

            var web = new HtmlWeb();
            var document = web.Load(url);

            var acceptableTags = new String[] {  };

            var nodes = new Queue<HtmlNode>(document.DocumentNode.SelectNodes("./*|./text()"));
            while (nodes.Count > 0)
            {
                var node = nodes.Dequeue();
                var parentNode = node.ParentNode;

                if (!acceptableTags.Contains(node.Name) && node.Name != "#text")
                {

                    var rRemScript = new Regex(@"<script[^>]*>[\s\S]*?</script>");
                    var rRemComments = new Regex(@"<!--[^>]*>[\s\S]*?-->");
                    var rRemHead = new Regex(@"<head[^>]*>[\s\S]*?</head>");
                    node.InnerHtml = rRemScript.Replace(node.InnerHtml, "");
                    node.InnerHtml = rRemComments.Replace(node.InnerHtml, "");
                    node.InnerHtml = rRemHead.Replace(node.InnerHtml, "");
                    var childNodes = node.SelectNodes("./*|./text()");

                    if (childNodes != null)
                    {
                        foreach (var child in childNodes)
                        {
                            nodes.Enqueue(child);
                            parentNode.InsertBefore(child, node);
                        }
                    }

                    parentNode.RemoveChild(node);

                }
            }

            var result = document.DocumentNode.InnerHtml.Replace("\t", "").Replace("\r\n", "\n").Replace("\\n", "");
            result = Regex.Replace(result, @"\n{2,}", @" ");
            result = Regex.Replace(result, @"\s{2,}", @" ");
            return result;

        }
    }
}
