import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Point2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.Timer;

public class Meteors extends JPanel implements ActionListener,MouseListener,KeyListener{
	public final int WIDTH=640, HEIGHT=480;
	public Random rand;
	//public Renderer renderer;
	BubbleGame bgame;
	int  num_of_bubbles=500;
	Ellipse2D[] bubbles=new Ellipse2D[num_of_bubbles];
	int[] bubblesX=new int[num_of_bubbles];
	Float[] bubblesY=new Float[num_of_bubbles];
	int[] bubblesw=new int[num_of_bubbles],bubblesh=new int[num_of_bubbles];
	Color[] colors= {Color.CYAN,Color.DARK_GRAY,Color.BLUE,Color.lightGray,Color.white};
	Ellipse2D bubble;
	Float bubbleY=100f;
	int bubbleX;
	Point2D mouse_pt;
	int speed,pl_speed=3;
	int playerX,playerY,player_w=20,player_h=20;
	boolean left=false,right=false,up=false,down=false,fire=true,cleared=false,transition=true;
	Map<Ellipse2D,Color> mets_colors=new HashMap();
	int time,score,bulletX,bulletY,bulletCount,health,level;
	Rectangle bullet;
	List<Rectangle> bullets=new ArrayList();
	BufferedImage player_img;
	private boolean gameOver;
	FontMetrics fm;
	Font font=new Font("Arial",Font.PLAIN,20);
	String msg1="GAME OVER",msg2="Click to play again!";
	
	public Meteors() {
		JFrame f = new JFrame();
		Timer timer = new Timer(20,this);
		//renderer=new Renderer();
		rand=new Random();
		loadImgs();
		
		f.add(this);
		f.setTitle("Meteor'z!");
		f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		f.addMouseListener(this);
		f.addKeyListener(this);
		f.setResizable(true);
		f.setVisible(true);
		f.setMinimumSize(new Dimension(WIDTH,HEIGHT));
		f.setMaximumSize(new Dimension(WIDTH,HEIGHT));
		f.pack();
		//reload();
		timer.start();
		init();
	}
	
	private void init() {
		bubbleX=rand.nextInt(0,WIDTH-20);
		bubble=new Ellipse2D.Float(bubbleX,bubbleY,20f,20f);
		playerX=WIDTH/2;
		playerY=HEIGHT-100;
		bulletCount=7;
		health=100;
		time=0;
		score=0;
		level=0;
		gameOver=false;
		genBubbles();
	}

	private boolean reload() {
		for(Rectangle bullet:bullets) {
			if(bullet.getY()>0)
				return false;
		}
		return true;
	}
	
	private void genBubbles() {
		
		for(int i=0;i<bubblesX.length;i++) {
			bubblesX[i]=rand.nextInt(-600,WIDTH-200);
			bubblesY[i]=rand.nextFloat(-700f, -30f);
			bubblesw[i]=rand.nextInt(18,22);
			bubblesh[i]=rand.nextInt(18,22);
			bubbles[i]=new Ellipse2D.Float(bubblesX[i], bubblesY[i], bubblesw[i], bubblesh[i]);
			mets_colors.put(bubbles[i], colors[rand.nextInt(5)]);
		}
	}

	protected void paintComponent(Graphics g) {
		super.paintComponent(g);
		this.repaint(g);
	}
	
	private void repaint(Graphics g) {
		g.setColor(Color.black);
		g.fillRect(0, 0, WIDTH, HEIGHT);
		
		if(!gameOver) {
		Graphics2D g2d=(Graphics2D) g;
		g2d.setColor(Color.magenta);
		g2d.fill(bubble);
		//System.out.println("DRAWING");
		for(Ellipse2D bub:bubbles) {
			g2d.setColor(colors[rand.nextInt(5)]);
			g2d.setColor(mets_colors.get(bub));
			g2d.fill(bub);
		}
		
		g.setColor(Color.yellow);
		//g.setFont(new Font("Arial",14,Font.PLAIN));
		g.drawString("SCORE: "+score, 400, 15);
		
		g.setColor(Color.orange);
		g.fillOval(playerX, playerY, player_w, player_h);
		//Draw bullet
		g.setColor(Color.white);
		//g.fillRect(bulletX, bulletY, 2, 2);
		for(Rectangle bullet:bullets)
			g.fillRect((int)bullet.getX(),(int)bullet.getY(), 2, 2);
		
		g.setColor(Color.GREEN);
		g.fillRect(WIDTH-100,15,health,7);
		//if(transition)
		g.drawString("LEVEL "+level, 10, 15);
		//g.drawImage(player_img, 100, 100,player_img.getWidth(),player_img.getHeight(), null);
		}
		else {
			g.setColor(Color.red);
			g.setFont(font);
			fm=g.getFontMetrics();
			int str_w1=fm.stringWidth(msg1);
			int str_w2=fm.stringWidth(msg2);
			int str_h=fm.getHeight();
			g.drawString(msg1, WIDTH/2-str_w1/2, HEIGHT/2-str_h/2);
			g.drawString(msg2, WIDTH/2-str_w2/2, HEIGHT/2-str_h/2+15);
		}
		
		g.dispose();
	}

	private void loadImgs() {
		try {
			player_img=ImageIO.read(new File("C:\\Users\\ricar\\Documents\\workspace-spring-tool-suite-4-4.15.3.RELEASE\\Piano-master\\src\\res\\player.png"));
		}catch(Exception e) {
			e.printStackTrace();
		}
	}

	@Override
	public void keyTyped(KeyEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void keyPressed(KeyEvent e) {
		int key=e.getKeyCode();
		System.out.println(bulletCount+", "+fire);
		
		switch(key){
			case 32:
				if(fire) {
					//fire=true;
					bulletX=playerX+10;
					bulletY=playerY+10;
					bullets.add(new Rectangle(playerX+10,playerY+10,2,2));
					bulletCount--;
				}
				break;
			case 37:
				left=true;
				//System.out.print(":SET");
				//playerX-=pl_speed;
				break;
			case 38:
				up=true;
				//playerY-=pl_speed;
				break;
			case 39:
				right=true;
				//playerX+=pl_speed;
				break;
			case 40:
				down=true;
				//playerY+=pl_speed;
				break;
			default:
				break;
			}
	}

	@Override
	public void keyReleased(KeyEvent e) {
		int key=e.getKeyCode();
		
		switch(key){
		case 37:
			left=false;
			System.out.print(":Release");
			//playerX-=pl_speed;
			break;
		case 38:
			up=false;
			//playerY-=pl_speed;
			break;
		case 39:
			right=false;
			//playerX+=pl_speed;
			break;
		case 40:
			down=false;
			//playerY+=pl_speed;
			break;
		default:
			break;
		}
	}

	@Override
	public void mouseClicked(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mousePressed(MouseEvent e) {
		System.out.println(e.getPoint());
		//System.out.println(bubble.getX()+", "+bubble.getY());
		mouse_pt=new Point.Double((double)e.getX(),(double) e.getY());
		
		if(gameOver) {
			gameOver=false;
			bullets.clear();
			init();}
	}

	@Override
	public void mouseReleased(MouseEvent e) {
		mouse_pt=null;
	}

	@Override
	public void mouseEntered(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseExited(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		
		if(!gameOver) {
		bubble.setFrame(bubbleX, bubbleY, 20, 20);
		bubbleY+=1;
		//Movement
		if(left)
			playerX-=pl_speed;
		if(right)
			playerX+=pl_speed;
		if(up)
			playerY-=pl_speed;
		if(down)
			playerY+=pl_speed;
		//Offbounds
		if(playerX+20>WIDTH)
			playerX=WIDTH-20;
		else if(playerX<0)
			playerX=0;
		else if(playerY+20>HEIGHT)
			playerY=HEIGHT-20;
		else if(playerY<0)
			playerY=0;
		
		if(!cleared) {
			bulletY-=5;
			bullet=new Rectangle(bulletX,bulletY,2,2);
			for(Rectangle bullet:bullets) 
				bullet.setFrame(bullet.getX(),bullet.getY()-5,2,2);
		}
		/*if(bulletY<0)
			fire=false;*/
		if(bulletCount==0)
			fire=false;
		else
			fire=true;
		
		for(Ellipse2D bub:bubbles) {
			speed=rand.nextInt(1,6);
			bub.setFrame(bub.getX()+speed,bub.getY()+speed,bub.getWidth(),bub.getHeight());
			//System.out.println(bub.getBounds().toString());
			if(bub.intersects(new Rectangle(playerX,playerY,player_w,player_h)))
				health-=1;
		}
		
		Point2D pt=new Point.Double(10,240.0);
		for(Ellipse2D bub:bubbles) {
			for(Rectangle bullet:bullets)
				if(fire==true && bullet.intersects(bub.getBounds())) {
					bub.setFrame(0, 10000, 1, 1);
					score++;
				}
		}
		
		if(bulletCount==0&&reload()) bulletCount=5;
		
		//OFFBOUNDS
		if(playerX<0)
			playerX=0;
		if(playerX+player_w>WIDTH)
			playerX=WIDTH-player_w;
		
		if(bubbleY>HEIGHT) {
			bubbleY=-100f;
			transition=true;
			level+=1;
			score+=level*2;
		}
		else if(bubbleY==50) {
			genBubbles();
			health+=10;
		}else if(bubbleY<50)
			transition=false;
		//GAMEOVER
		if(health<=0)
			gameOver=true;
		}
		
		//System.out.println("RUNNING");
		this.repaint();
	}
	
	public static void main(String[] args) {
		new Meteors();
	}
}