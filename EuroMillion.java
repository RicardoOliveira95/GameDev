import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

public class EuroMillion {
	Random rand=new Random();
	private ArrayList<Integer> keys = new ArrayList<>();
	int[] nums = new int[5];
	int[] stars = new int[2];
	int num=0;

	public EuroMillion() {
		fillNumbers();
		//sortKey();
		sortKey2();
		System.out.println("Sorted key is: "+keys.toString());
	}

	private void fillNumbers() {
		for(int i=1;i<50;i++) {
			keys.add(i);
		}
	}

	private void sortKey2() {
		Collections.shuffle(keys);
		for(int i=1;i<5;i++) {
			num = keys.get(i);
			nums[i]=num;
		}
		int i=0;
		while(i<2) {
			num=rand.nextInt(11)+1;
			stars[i]=num;
			if(stars[0]!=stars[1]) {
				break;
			}
		}
	}

	private void sortKey() {
		rand = new Random();
		//Numbers
		for(int i=0;i<nums.length;i++) {
		int num = rand.nextInt(49)+1;
		System.out.println(num);
		for(int offSet=0;offSet<i;offSet++) {
			if(nums[i]!=nums[i-offSet]) {
			nums[i]=num;
			System.out.println(num);
			keys.add(num);}
		}
		}
		int star1 = rand.nextInt(12);
		int star2=star1;
		while(star1==star2) {
			star2 = rand.nextInt(12);
		}
		keys.add(star1);
		keys.add(star2);
	}

	public static void main(String[] args) {
		new EuroMillion();
	}

}
