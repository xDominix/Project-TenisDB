using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TennisApp
{
    internal class Match
    {
        public int ID { get; set; }

        public ICollection<User> Players { get; set; }

        public String score { get; set; }
        public Boolean isFinished { get; set; }
        public ICollection<Reservation> Reservations { get; set; }
    }
}
