import java.util.Random;
import java.util.Scanner;

public class Double07 {
	int plBullets,cpuBullets=0;
	String move;
	int moveCpu;

	public Double07() {
		Scanner scan = new Scanner(System.in);
		while(true){
			System.out.println("Make move..");
			move = scan.nextLine();
			if(!makeMove(move)) System.out.print("PLAY AGAIN..");
			else {
				moveCpu = makeBotMove();
				if(checkWinner(moveCpu,move)) return;
			}
		}
	}

	private boolean checkWinner(int moveCpu, String move) {
		if(moveCpu==2&&move=="c") {
			System.out.println("CPU wins!");
			return true;
		}
		if(moveCpu==1&&move=="s") {
			System.out.println("Player wins!");
			return true;
		}
		return false;
	}

	private int makeBotMove() {
		String move;
		int num;
		Random rand = new Random();
		if(cpuBullets==0) {
			num = rand.nextInt(2);
			System.out.println(num);
		}else {
			num = rand.nextInt(3);
		}
		switch(num) {
		case 0:
			System.out.println("Defense.."); break;
		case 1:
			System.out.println("Charging..");
			cpuBullets+=1; break;
		case 2:
			System.out.println("Shooting!");
			cpuBullets-=1; break;
		}
		return num;
	}

	private boolean makeMove(String move) {
		System.out.println(move);
		switch(move) {
			case "s":
				if(plBullets>0) {
					plBullets-=1;
				}else {
					System.out.println("You have no bullets..");
					return false;
				}break;
			case "d":
				{System.out.println("Defense"); break;}
			case "c":
				{plBullets+=1; System.out.println("Charging.."); break;}
			default:
				System.out.println("Cannot detect your move, sorry..");
				return false;
		}
		return true;
	}

	public static void main(String[] args) {
		new Double07();
	}

}
