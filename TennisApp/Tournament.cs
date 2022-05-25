using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TennisApp
{
    internal class Tournament
    {
        public int ID { get; set; }
        public ICollection<User> Players { get; set; }
        public DateTime DateFrom { get; set; }
        public DateTime DateTo { get; set; }
        public ICollection<Reservation> Reservations { get; set; }
        public String winnerRewards { get; set; }
        public int minSkillLevel { get; set; }
    }
}
