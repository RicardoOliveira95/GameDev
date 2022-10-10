
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

import javax.swing.*;

import jm.util.Play;    
public class Puzzle implements Runnable{    
JFrame f;
public int count;
private String[] values = {"1","2","3","4","5","6","7","8","9"};;
String pl_1="X",pl_2="O";
int turn=0,moves=0,timer=0;
JButton[] btns;
boolean isGameOver;
boolean[] btn_show;
boolean selected_box;
Map<JButton,String> map_values=new HashMap();
JButton prev_btn;
ArrayList rand_values=new ArrayList();

Puzzle(){
	isGameOver=false;
    f=new JFrame();
    
    //Generate puzzle
    for(String number:values)
    	if(number!="9")
    		rand_values.add(number);
    
    Collections.shuffle(rand_values);
    
    JButton b1=new JButton((String)rand_values.get(0));    
    JButton b2=new JButton((String)rand_values.get(1));    
    JButton b3=new JButton((String)rand_values.get(2));    
    JButton b4=new JButton((String)rand_values.get(3));    
    JButton b5=new JButton((String)rand_values.get(4));    
    JButton b6=new JButton((String)rand_values.get(5));    
    JButton b7=new JButton((String)rand_values.get(6));    
    JButton b8=new JButton((String)rand_values.get(7));    
    JButton b9=new JButton("");    
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
    
    
    btn_show = new boolean[9];
    Thread thread = new Thread();
    thread.start();
    prev_btn=btns[8];
    prev_btn.setEnabled(false);;

    for(int i=0;i<btns.length;i++)
    	map_values.put(btns[i],values[i]);
    
    for(count=0;count<btns.length;count++) {
    	btns[count].addActionListener(new ActionListener() {

    		@Override
    		public void actionPerformed(ActionEvent e) {
    			JButton btn = (JButton) e.getSource();
    			String btn_label=btn.getLabel();
    			
    			if(btn.isEnabled() && playableCell(btn,prev_btn)) {
    				btn.setEnabled(false);
    				prev_btn.setEnabled(true);
    				prev_btn.setLabel(btn.getLabel());
    				btn.setLabel("");
    				prev_btn=btn;
    				moves++;
    			}
    			if(checkWin())
    				JOptionPane.showMessageDialog(f, "Win with ("+moves+") moves!");
    		} 
    	});
    }
}

protected boolean playableCell(JButton btn,JButton prev_btn) {
	System.out.println(map_values.get(prev_btn)+","+map_values.get(btn));
	if(Integer.parseInt(map_values.get(prev_btn))==Integer.parseInt(map_values.get(btn))-3
			||Integer.parseInt(map_values.get(prev_btn))==Integer.parseInt(map_values.get(btn))+3
			||Integer.parseInt(map_values.get(prev_btn))==Integer.parseInt(map_values.get(btn))+1
			||Integer.parseInt(map_values.get(prev_btn))==Integer.parseInt(map_values.get(btn))-1)
		return true;
	
	return false;
}

protected boolean checkWin() {
	for(int i=0;i<btns.length-1;i++) 
		//System.out.println(btns[i].getLabel()+","+values[i]);
		if(!(btns[i].getLabel()==values[i]))
			return false;
	return true;
}

public static void main(String[] args) {    
    new Puzzle();    
}


@Override
public void run() {
	// TODO Auto-generated method stub
	
}    
}   