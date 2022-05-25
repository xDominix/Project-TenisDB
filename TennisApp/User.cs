using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TennisApp
{
    internal class User
    {
        public int ID { get; set; }
        public ICollection<Match> Matches { get; set; }
        public String Email { get; set; }
        public String Password { get; set; }
        public int PhoneNumber { get; set; }
        public String Name { get; set; }
        public String Surname { get; set; }
        public DateTime BirthDate { get; set; }
        public String City { get; set; }
        public Boolean RightHanded { get; set; }
        public String Racket { get; set; }
        public String FavSurface { get; set; }
        public String FavClub { get; set; }
    }
}
