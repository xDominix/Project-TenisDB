using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace TennisApp.Migrations
{
    public partial class Init : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Courts",
                columns: table => new
                {
                    ID = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    Club = table.Column<string>(type: "TEXT", nullable: false),
                    CourtNumber = table.Column<int>(type: "INTEGER", nullable: false),
                    Surface = table.Column<string>(type: "TEXT", nullable: false),
                    Lights = table.Column<bool>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Courts", x => x.ID);
                });
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Courts");
        }
    }
}
