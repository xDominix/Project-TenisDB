using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TennisApp
{
    internal class Court
    {
        [Key]
        public int ID { get; set; }
        public string Club { get; set; }
        public int CourtNumber { get; set; }
        public string Surface { get; set; }
        public Boolean Lights { get; set; }

        public ICollection<Reservation> Reservations { get; set; }

    }
}
