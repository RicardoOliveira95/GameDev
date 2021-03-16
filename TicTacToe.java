import java.util.Random;
import java.util.Scanner;

public class TicTacToe {
	String[][] board = new String[3][3];
	private static final String P1="x",P2="o";
	private String winner;
	int scorep1,scorep2;

	public TicTacToe() {
		Scanner scan = new Scanner(System.in);
		System.out.println("Tic Tac Toe: you play first");
		emptyBoard();
		while(true) {
			System.out.println("Play in format: line/col: 12..");
			int moveRow = scan.nextInt();
			int moveCol = scan.nextInt();
			if(!playableMove(moveRow,moveCol)) System.out.println("Can't play there, play again..");
			makeMove(moveRow,moveCol);
			makeBotMove();
			if(checkWinner()) {
				System.out.println("Winner is: "+winner);
			}
			printBoard();
		}
	}

	private boolean checkWinner() {
		int j=0;  //CHECK ROWS
		for(int i=0;i<board.length;i++) {
			if(board[i][j]==board[i][j+1]&&board[i][j]==board[i][j+2]) {
				System.out.println("LINE: "+board[i][j]+board[i][j+1]+board[i][j+2]);
				winner = board[i][j]=="x" ? "Player1" : "Player2"; 
				return true;
			}
		}  //CHECK COLS
		for(int i=0;i<board[j].length;i++) {
			if(board[j][i]==board[j+1][i]&&board[j][i]==board[j+2][i]) {
				System.out.println("Column: "+board[j][i]+board[j+1][i]+board[j+2][i]);
				winner = board[i][j]=="x" ? "Player1" : "Player2"; 
				return true;
			}
		}
		int i=0;
		//CROSSES
		if(board[i][j]==board[i+1][j+1]&&board[i][j]==board[i+2][j+2]||board[i+2][j]==board[i+1][j+1]&&board[i+2][j]==board[i][j+2]) {
			winner = board[i][j]=="x" ? "Player1" : "Player2"; 
		return true;}
		return false;
	}

	private void makeBotMove() {
		// Dumb move
		Random rand = new Random();
		int moveRow = rand.nextInt(3);
		int moveCol = rand.nextInt(3);
		System.out.println(moveRow+moveCol);
		if(playableMove(moveRow,moveCol)) {
			board[moveRow][moveCol]=P2;
		} else { makeBotMove();}
	}

	private boolean playableMove(int moveRow, int moveCol) {
		if(board[moveRow][moveCol]==" ")
			return true;
		return false;
	}

	private void makeMove(int moveRow, int moveCol) {
		board[moveRow][moveCol]=P1;
	}

	private void printBoard() {
		for(int row=0;row<board.length;row++) {
			System.out.println();;
			for(int col=0;col<board[row].length;col++) {
				System.out.print("|"+board[row][col]+"|");
			}
		}System.out.println();
	}

	private void emptyBoard() {
		for(int row=0;row<board.length;row++) {
			System.out.println();
			for(int col=0;col<board[row].length;col++) {
				board[row][col]=" ";
				System.out.print("|"+board[row][col]+"|");
				//System.out.println();
			}
		}System.out.println();
	}

	public static void main(String[] args) {
		new TicTacToe();
	}

}
