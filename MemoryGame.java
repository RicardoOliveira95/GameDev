import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.HashMap;
import java.util.Map;

import javax.swing.*;

import jm.util.Play;    
public class MemoryGame implements Runnable{    
JFrame f;
public int count;
String pl_1="X",pl_2="O";
int turn=0,moves=0,timer=0;
JButton[] btns;
boolean isGameOver;
boolean[] btn_show;
boolean selected_box;
Map<JButton,String> map_values=new HashMap();
JButton prev_btn;
private String[] ordered_values= {"1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"};
private Map<JButton,String> ordered_btns=new HashMap();;

MemoryGame(){
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
    JButton b10=new JButton("10");    
    JButton b11=new JButton("11");    
    JButton b12=new JButton("12");    
    JButton b13=new JButton("13");    
    JButton b14=new JButton("14");    
    JButton b15=new JButton("15");    
    JButton b16=new JButton("16");
     // adding buttons to the frame       
    f.add(b1); f.add(b2); f.add(b3);  
    f.add(b4); f.add(b5); f.add(b6);  
    f.add(b7); f.add(b8); f.add(b9); 
    f.add(b10);  f.add(b11); f.add(b12); 
    f.add(b13);  f.add(b14); f.add(b15); f.add(b16);
  
    // setting grid layout of 4 rows and 4 columns    
    f.setLayout(new GridLayout(4,4));    
    f.setSize(300,300);    
    f.setVisible(true);
    
    btns = new JButton[16];
    btns[0]=b1;
    btns[1]=b2;
    btns[2]=b3;
    btns[3]=b4;
    btns[4]=b5;
    btns[5]=b6;
    btns[6]=b7;
    btns[7]=b8;
    btns[8]=b9;
    btns[9]=b10;
    btns[10]=b11;
    btns[11]=b12;
    btns[12]=b13;
    btns[13]=b14;
    btns[14]=b15;
    btns[15]=b16;
    
    String[] values = {"A","B","C","C","D","A","B","D","E","F","E","G","G","F","H","H","E"};
    
    btn_show = new boolean[9];
    Thread thread = new Thread();
    thread.start();

    for(int i=0;i<btns.length;i++) {
    	map_values.put(btns[i],values[i]);
    	ordered_btns.put(btns[i], ordered_values[i]);
    }
    
    for(count=0;count<btns.length;count++) {
    	btns[count].addActionListener(new ActionListener() {

    		@Override
    		public void actionPerformed(ActionEvent e) {
    			moves++;
    			JButton btn = (JButton) e.getSource();
    			String btn_label=btn.getLabel();
    			timer=0;
				
    			if(!selected_box) {
				 btn.setEnabled(false);
				 btn.setLabel(map_values.get(btn));
				 selected_box=true;
				 prev_btn=btn;
    			}
    			else {
    				btn.setLabel(map_values.get(btn));
    				if (!(prev_btn.getLabel()==btn.getLabel())){
	    				prev_btn.setEnabled(true);
	    				prev_btn.setLabel(ordered_btns.get(prev_btn));
	    				btn.setEnabled(false);
	    				prev_btn=btn;
	    				selected_box=true;
    				}else {
    					btn.setEnabled(false);
    					selected_box=false;
    				}
    			}if(checkWin()) JOptionPane.showMessageDialog(f, "Win with ("+moves+") moves!");
    		}	
    	});
    }
}

protected boolean checkWin(){
	for(JButton btn:btns)
		if(btn.isEnabled())
			return false;
	return true;
}

public static void main(String[] args) {    
    new MemoryGame();    
}


@Override
public void run() {
	// TODO Auto-generated method stub
	
}    
}   