using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace TennisApp.Migrations
{
    public partial class all4 : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Matches_Users_UserID",
                table: "Matches");

            migrationBuilder.DropForeignKey(
                name: "FK_Reservations_Matches_MatchID",
                table: "Reservations");

            migrationBuilder.DropIndex(
                name: "IX_Matches_UserID",
                table: "Matches");

            migrationBuilder.DropColumn(
                name: "Match",
                table: "Reservations");

            migrationBuilder.DropColumn(
                name: "UserID",
                table: "Matches");

            migrationBuilder.AlterColumn<int>(
                name: "MatchID",
                table: "Reservations",
                type: "INTEGER",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "INTEGER",
                oldNullable: true);

            migrationBuilder.CreateTable(
                name: "MatchUser",
                columns: table => new
                {
                    MatchesID = table.Column<int>(type: "INTEGER", nullable: false),
                    PlayersID = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_MatchUser", x => new { x.MatchesID, x.PlayersID });
                    table.ForeignKey(
                        name: "FK_MatchUser_Matches_MatchesID",
                        column: x => x.MatchesID,
                        principalTable: "Matches",
                        principalColumn: "ID",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_MatchUser_Users_PlayersID",
                        column: x => x.PlayersID,
                        principalTable: "Users",
                        principalColumn: "ID",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_MatchUser_PlayersID",
                table: "MatchUser",
                column: "PlayersID");

            migrationBuilder.AddForeignKey(
                name: "FK_Reservations_Matches_MatchID",
                table: "Reservations",
                column: "MatchID",
                principalTable: "Matches",
                principalColumn: "ID",
                onDelete: ReferentialAction.Cascade);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Reservations_Matches_MatchID",
                table: "Reservations");

            migrationBuilder.DropTable(
                name: "MatchUser");

            migrationBuilder.AlterColumn<int>(
                name: "MatchID",
                table: "Reservations",
                type: "INTEGER",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "INTEGER");

            migrationBuilder.AddColumn<int>(
                name: "Match",
                table: "Reservations",
                type: "INTEGER",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<int>(
                name: "UserID",
                table: "Matches",
                type: "INTEGER",
                nullable: true);

            migrationBuilder.CreateIndex(
                name: "IX_Matches_UserID",
                table: "Matches",
                column: "UserID");

            migrationBuilder.AddForeignKey(
                name: "FK_Matches_Users_UserID",
                table: "Matches",
                column: "UserID",
                principalTable: "Users",
                principalColumn: "ID");

            migrationBuilder.AddForeignKey(
                name: "FK_Reservations_Matches_MatchID",
                table: "Reservations",
                column: "MatchID",
                principalTable: "Matches",
                principalColumn: "ID");
        }
    }
}
