import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;

import jm.util.Play;    
public class TicTacToe{    
JFrame f;
public int count;
String pl_1="X",pl_2="O";
int turn=1,moves=0;
JButton[] btns;
boolean isGameOver;

TicTacToe(){
	isGameOver=false;
    f=new JFrame();    
    JButton b1=new JButton("1");    
    JButton b2=new JButton("2");    
    JButton b3=new JButton("3");    
    JButton b4=new JButton("4");    
    JButton b5=new JButton("5");    
    JButton b6=new JButton("6");    
    JButton b7=new JButton("7");    
    JButton b8=new JButton("8");    
    JButton b9=new JButton("9");    
     // adding buttons to the frame       
    f.add(b1); f.add(b2); f.add(b3);  
    f.add(b4); f.add(b5); f.add(b6);  
    f.add(b7); f.add(b8); f.add(b9);    
  
    // setting grid layout of 3 rows and 3 columns    
    f.setLayout(new GridLayout(3,3));    
    f.setSize(300,300);    
    f.setVisible(true);
    
    btns = new JButton[9];
    btns[0]=b1;
    btns[1]=b2;
    btns[2]=b3;
    btns[3]=b4;
    btns[4]=b5;
    btns[5]=b6;
    btns[6]=b7;
    btns[7]=b8;
    btns[8]=b9;
    
    for(count=0;count<btns.length;count++) {
    	btns[count].addActionListener(new ActionListener() {

    		@Override
    		public void actionPerformed(ActionEvent e) {
    			turn++;
    			JButton btn = (JButton) e.getSource();
    			System.out.println(btn.getParent().getComponentZOrder(btn));
    			if(turn%2==0) {
    				if(!(btn.getLabel()==pl_1 || btn.getLabel()==pl_2)) {
    					btn.setLabel(pl_1);
    					btn.setBackground(Color.blue);
    				}
    				
    				else
    					turn--;
    			}
    			else {
    				if(!(btn.getLabel()==pl_1 || btn.getLabel()==pl_2)) {
    					btn.setLabel(pl_2);
    					btn.setBackground(Color.red);
    				}
    					
    				else 
    					turn--;
    			}
    			
    			if(checkWin(btn.getLabel())==1)
    				JOptionPane.showMessageDialog(f, "Player 1 wins!");
    			
    			else if(checkWin(btn.getLabel())==2)
    				JOptionPane.showMessageDialog(f, "Player 2 wins!");
    			
    			//System.out.println("WINNER: "+checkWin(btn.getLabel()));
    		}	
    	});
    }
}

protected int checkWin(String label) {
	//horizontal check
	if((btns[0].getLabel()==btns[1].getLabel() && btns[0].getLabel()==btns[2].getLabel())||(btns[3].getLabel()==btns[4].getLabel() && btns[3].getLabel()==btns[5].getLabel())||(btns[6].getLabel()==btns[7].getLabel() && btns[6].getLabel()==btns[8].getLabel())) {
		if(label==pl_1)
			return 1;
		else if(label==pl_2)
			return 2;
	}
	//vertical check
	if((btns[0].getLabel()==btns[3].getLabel() && btns[0].getLabel()==btns[6].getLabel())||(btns[1].getLabel()==btns[4].getLabel() && btns[1].getLabel()==btns[7].getLabel())||(btns[2].getLabel()==btns[5].getLabel() && btns[2].getLabel()==btns[8].getLabel())) {
		if(label==pl_1)
			return 1;
		else if(label==pl_2)
			return 2;
	}
	//diagonal check
	if((btns[0].getLabel()==btns[4].getLabel() && btns[0].getLabel()==btns[8].getLabel())||(btns[2].getLabel()==btns[4].getLabel() && btns[2].getLabel()==btns[6].getLabel())) {
		if(label==pl_1)
			return 1;
		else if(label==pl_2)
			return 2;
	}
	
	return 0;
}

public static void main(String[] args) {    
    new TicTacToe();    
}    
}   
