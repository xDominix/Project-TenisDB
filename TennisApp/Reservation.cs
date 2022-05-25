using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TennisApp
{
    internal class Reservation
    {
        public int ID { get; set; }
        public User User { get; set; }
        public DateTime DateFrom { get; set; }
        public DateTime DateTo { get; set; }
        public Match Match { get; set; }
    }
}
