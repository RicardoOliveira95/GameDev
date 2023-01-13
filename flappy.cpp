#include <SDL.h>
#include <SDL_image.h>
#include <stdio.h>
#include <string>
#include <string.h>

const static int SCREEN_W = 640, SCREEN_H = 480;

class LTexture {
public:
	LTexture();
	~LTexture();
	bool loadFromFile(std::string path);
	void free();
	//Loads image into pixel buffer
	bool loadPixelsFromFile(std::string path);

	//Creates image from preloaded pixels
	bool loadFromPixels();
	//Sets
	void setColor(Uint8 r, Uint8 g, Uint8 b);
	void setBlendMode(SDL_BlendMode blending);
	void setAlpha(Uint8 alpha);
	void render(int x, int y, SDL_Rect* clip = NULL, double ang = 0.0, SDL_Point* center = NULL, SDL_RendererFlip flip = SDL_FLIP_NONE);
	//Gets
	int getWidth();
	int getHeight();
	//Pixel accessors
	Uint32* getPixels32();
	Uint32 getPixel32(Uint32 x, Uint32 y);
	Uint32 getPitch32();
private:
	SDL_Texture* mTex;
	SDL_Surface* mSurfacePixels;
	int m_w, m_h;
};

class Dot {
public:
	static const int DOT_W = 15, DOT_H = 15, DOT_VEL = 4;
	Dot();
	void handleEvent(SDL_Event& evt);
	void move();
	void render(SDL_Rect* clip=NULL);
private:
	int mPosX, mPosY, mVelX, mVelY;
};

//Our bitmap font
class LBitmapFont
{
public:
	//The default constructor
	LBitmapFont();

	//Generates the font
	bool buildFont(std::string path);

	//Deallocates font
	void free();

	//Shows the text
	void renderText(int x, int y, std::string text);

private:
	//The font texture
	LTexture mFontTexture;

	//The individual characters in the surface
	SDL_Rect mChars[256];

	//Spacing Variables
	int mNewLine, mSpace;

	//Surface pixels
	SDL_Surface* mSurfacePixels;
};
//Methods
bool init();
bool loadMedia();
void close();
//Vars
SDL_Window* gWin = NULL;
SDL_Renderer* gRenderer = NULL;
LTexture gDotTex, gBckgTex, gFloorTex;
//Walking animation
const int WALKING_ANIMATION_FRAMES = 3;
SDL_Rect gSpriteClips[WALKING_ANIMATION_FRAMES];
LTexture gSpriteSheetTexture;
LBitmapFont gBitmapFont;
int time = 0;
char time_msg[20] = "Time: ";

LTexture::LTexture() {
	//Constructor
	mTex = NULL;
	mSurfacePixels = NULL;
	m_w = 0;
	m_h = 0;
}

LTexture::~LTexture() {
	free();
}

LBitmapFont::LBitmapFont(){
	//Initialize variables(constructor)
	mNewLine = 0;
	mSpace = 0;
}

/*bool LTexture::loadFromFile(std::string path) {
	free();
	SDL_Texture* newTex = NULL;
	//Load img at given path
	SDL_Surface* loadedSurf = IMG_Load(path.c_str());
	if (loadedSurf == NULL)
		printf("Unable to load image at %s! SDL_image Error: %s\n", path.c_str(), IMG_GetError());
	else {
		//Color key img
		SDL_SetColorKey(loadedSurf, SDL_TRUE, SDL_MapRGB(loadedSurf->format, 0, 0xFF, 0xFF));
		//Create tex from surface pixels
		newTex = SDL_CreateTextureFromSurface(gRenderer, loadedSurf);
		if (newTex == NULL)
			printf("Unable to create texture from %s! SDL Error: %s\n", path.c_str(), SDL_GetError());
		else {
			m_w = loadedSurf->w;
			m_h = loadedSurf->h;
		}
		SDL_FreeSurface(loadedSurf);
	}
	mTex = newTex;
	return mTex != NULL;
}*/

bool LTexture::loadFromFile(std::string path)
{
	//Load pixels
	if (!loadPixelsFromFile(path))
	{
		printf("Failed to load pixels for %s!\n", path.c_str());
	}
	else
	{
		//Load texture from pixels
		if (!loadFromPixels())
		{
			printf("Failed to texture from pixels from %s!\n", path.c_str());
		}
	}

	//Return success
	return mTex != NULL;
}

bool LTexture::loadPixelsFromFile(std::string path)
{
	//Free preexisting assets
	free();

	//Load image at specified path
	SDL_Surface* loadedSurface = IMG_Load(path.c_str());
	if (loadedSurface == NULL)
	{
		printf("Unable to load image %s! SDL_image Error: %s\n", path.c_str(), IMG_GetError());
	}
	else
	{
		//Convert surface to display format
		mSurfacePixels = SDL_ConvertSurfaceFormat(loadedSurface, SDL_GetWindowPixelFormat(gWin), 0);
		if (mSurfacePixels == NULL)
		{
			printf("Unable to convert loaded surface to display format! SDL Error: %s\n", SDL_GetError());
		}
		else
		{
			//Get image dimensions
			m_w = mSurfacePixels->w;
			m_h = mSurfacePixels->h;
		}

		//Get rid of old loaded surface
		SDL_FreeSurface(loadedSurface);
	}

	return mSurfacePixels != NULL;
}

bool LTexture::loadFromPixels()
{
	//Only load if pixels exist
	if (mSurfacePixels == NULL)
	{
		printf("No pixels loaded!");
	}
	else
	{
		//Color key image
		SDL_SetColorKey(mSurfacePixels, SDL_TRUE, SDL_MapRGB(mSurfacePixels->format, 0, 0xFF, 0xFF));

		//Create texture from surface pixels
		mTex = SDL_CreateTextureFromSurface(gRenderer, mSurfacePixels);
		if (mTex == NULL)
		{
			printf("Unable to create texture from loaded pixels! SDL Error: %s\n", SDL_GetError());
		}
		else
		{
			//Get image dimensions
			m_w = mSurfacePixels->w;
			m_h = mSurfacePixels->h;
		}

		//Get rid of old loaded surface
		SDL_FreeSurface(mSurfacePixels);
		mSurfacePixels = NULL;
	}

	//Return success
	return mTex != NULL;
}

void LTexture::free() {
	//Clear tex
	if (mTex != NULL) {
		SDL_DestroyTexture(mTex);
		mTex = NULL;
		m_w = 0;
		m_h = 0;
	}
	if (mSurfacePixels != NULL) {
		mSurfacePixels = NULL;
		SDL_FreeSurface(mSurfacePixels);
	}
}

void LTexture::setColor(Uint8 r, Uint8 g, Uint8 b) {
	SDL_SetTextureColorMod(mTex, r, g, b);
}

void LTexture::setBlendMode(SDL_BlendMode blending) {
	SDL_SetTextureBlendMode(mTex, blending);
}

void LTexture::setAlpha(Uint8 alpha) {
	SDL_SetTextureAlphaMod(mTex, alpha);
}

void LTexture::render(int x, int y, SDL_Rect* clip, double ang, SDL_Point* center, SDL_RendererFlip flip) {
	//Mask
	SDL_Rect renderQuad = { x,y,m_w,m_h };
	if (clip != NULL) {
		renderQuad.w = clip->w;
		renderQuad.h = clip->h;
	}
	//Render to screen
	SDL_RenderCopyEx(gRenderer, mTex, clip, &renderQuad, ang, center, flip);
}

int LTexture::getWidth() {
	return m_w;
}

int LTexture::getHeight() {
	return m_h;
}

Uint32* LTexture::getPixels32()
{
	Uint32* pixels = NULL;

	if (mSurfacePixels != NULL)
	{
		pixels = static_cast<Uint32*>(mSurfacePixels->pixels);
	}

	return pixels;
}

Uint32 LTexture::getPixel32(Uint32 x, Uint32 y)
{
	//Convert the pixels to 32 bit
	Uint32* pixels = static_cast<Uint32*>(mSurfacePixels->pixels);

	//Get the pixel requested
	return pixels[(y * getPitch32()) + x];
}

Uint32 LTexture::getPitch32()
{
	Uint32 pitch = 0;

	if (mSurfacePixels != NULL)
	{
		pitch = mSurfacePixels->pitch / 4;
	}

	return pitch;
}

Dot::Dot() {
	//Init vars
	mPosX = 0; mPosY = 0;
	mVelX = 0; mVelY = 0;
}

void Dot::handleEvent(SDL_Event& evt) {
	//Key press
	if (evt.type == SDL_KEYDOWN && evt.key.repeat == 0)
		switch (evt.key.keysym.sym) {
		case SDLK_w: mVelY -= DOT_VEL; break;
		case SDLK_s: mVelY += DOT_VEL; break;
		case SDLK_a: mVelX -= DOT_VEL; break;
		case SDLK_d: mVelX += DOT_VEL; break;
		}
	//Key release
	else if (evt.type == SDL_KEYUP && evt.key.repeat == 0)
		switch (evt.key.keysym.sym) {
		case SDLK_w: mVelY += DOT_VEL; break;
		case SDLK_s: mVelY -= DOT_VEL; break;
		case SDLK_a: mVelX += DOT_VEL; break;
		case SDLK_d: mVelX -= DOT_VEL; break;
		}
}

void Dot::move() {
	//Update dot pos
	mPosX += mVelX;
	mPosY += mVelY;
	
	//Offbounds
	if ((mPosX < 0) || (mPosX + DOT_W > SCREEN_W))
		mPosX -= mVelX;
	else if ((mPosY < 0) || (mPosY + DOT_H +70 > SCREEN_H))
		mPosY -= mVelY;
	else
		mPosY += 2;
}

void Dot::render(SDL_Rect* clip) {
	//gDotTex.render(mPosX, mPosY);
	gSpriteSheetTexture.render(mPosX, mPosY,clip);
}

bool LBitmapFont::buildFont(std::string path)
{
	//Get rid of preexisting texture
	free();

	//Load bitmap image
	bool success = true;
	if (!mFontTexture.loadPixelsFromFile(path))
	{
		printf("Unable to load bitmap font surface!\n");
		success = false;
	}
	else
	{
		//Get the background color
		Uint32 bgColor = mFontTexture.getPixel32(0, 0);

		//Set the cell dimensions
		int cellW = mFontTexture.getWidth() / 16;
		int cellH = mFontTexture.getHeight() / 16;

		//New line variables
		int top = cellH;
		int baseA = cellH;

		//The current character we're setting
		int currentChar = 0;

		//Go through the cell rows
		for (int rows = 0; rows < 16; ++rows)
		{
			//Go through the cell columns
			for (int cols = 0; cols < 16; ++cols)
			{
				//Set the character offset
				mChars[currentChar].x = cellW * cols;
				mChars[currentChar].y = cellH * rows;

				//Set the dimensions of the character
				mChars[currentChar].w = cellW;
				mChars[currentChar].h = cellH;

				//Find Left Side
				//Go through pixel columns
				for (int pCol = 0; pCol < cellW; ++pCol)
				{
					//Go through pixel rows
					for (int pRow = 0; pRow < cellH; ++pRow)
					{
						//Get the pixel offsets
						int pX = (cellW * cols) + pCol;
						int pY = (cellH * rows) + pRow;

						//If a non colorkey pixel is found
						if (mFontTexture.getPixel32(pX, pY) != bgColor)
						{
							//Set the x offset
							mChars[currentChar].x = pX;

							//Break the loops
							pCol = cellW;
							pRow = cellH;
						}
					}
				}

				//Find Right Side
				//Go through pixel columns
				for (int pColW = cellW - 1; pColW >= 0; --pColW)
				{
					//Go through pixel rows
					for (int pRowW = 0; pRowW < cellH; ++pRowW)
					{
						//Get the pixel offsets
						int pX = (cellW * cols) + pColW;
						int pY = (cellH * rows) + pRowW;

						//If a non colorkey pixel is found
						if (mFontTexture.getPixel32(pX, pY) != bgColor)
						{
							//Set the width
							mChars[currentChar].w = (pX - mChars[currentChar].x) + 1;

							//Break the loops
							pColW = -1;
							pRowW = cellH;
						}
					}
				}

				//Find Top
				//Go through pixel rows
				for (int pRow = 0; pRow < cellH; ++pRow)
				{
					//Go through pixel columns
					for (int pCol = 0; pCol < cellW; ++pCol)
					{
						//Get the pixel offsets
						int pX = (cellW * cols) + pCol;
						int pY = (cellH * rows) + pRow;

						//If a non colorkey pixel is found
						if (mFontTexture.getPixel32(pX, pY) != bgColor)
						{
							//If new top is found
							if (pRow < top)
							{
								top = pRow;
							}

							//Break the loops
							pCol = cellW;
							pRow = cellH;
						}
					}
				}

				//Find Bottom of A
				if (currentChar == 'A')
				{
					//Go through pixel rows
					for (int pRow = cellH - 1; pRow >= 0; --pRow)
					{
						//Go through pixel columns
						for (int pCol = 0; pCol < cellW; ++pCol)
						{
							//Get the pixel offsets
							int pX = (cellW * cols) + pCol;
							int pY = (cellH * rows) + pRow;

							//If a non colorkey pixel is found
							if (mFontTexture.getPixel32(pX, pY) != bgColor)
							{
								//Bottom of a is found
								baseA = pRow;

								//Break the loops
								pCol = cellW;
								pRow = -1;
							}
						}
					}
				}

				//Go to the next character
				++currentChar;
			}
		}

		//Calculate space
		mSpace = cellW / 2;

		//Calculate new line
		mNewLine = baseA - top;

		//Lop off excess top pixels
		for (int i = 0; i < 256; ++i)
		{
			mChars[i].y += top;
			mChars[i].h -= top;
		}

		//Create final texture
		if (!mFontTexture.loadFromPixels())
		{
			printf("Unable to create font texture!\n");
			success = false;
		}
	}

	return success;
}

void LBitmapFont::free()
{
	mFontTexture.free();
}

void LBitmapFont::renderText(int x, int y, std::string text)
{
	//If the font has been built
	if (mFontTexture.getWidth() > 0)
	{
		//Temp offsets
		int curX = x, curY = y;

		//Go through the text
		for (int i = 0; i < text.length(); ++i)
		{
			//If the current character is a space
			if (text[i] == ' ')
			{
				//Move over
				curX += mSpace;
			}
			//If the current character is a newline
			else if (text[i] == '\n')
			{
				//Move down
				curY += mNewLine;

				//Move back
				curX = x;
			}
			else
			{
				//Get the ASCII value of the character
				int ascii = (unsigned char)text[i];

				//Show the character
				mFontTexture.render(curX, curY, &mChars[ascii]);

				//Move over the width of the character with one pixel of padding
				curX += mChars[ascii].w + 1;
			}
		}
	}
}

bool init() {
	//Init flag
	bool success = true;
	//Init SDL
	if (SDL_Init(SDL_INIT_VIDEO) < 0) {
		printf("SDL could not initialize! SDL Error: %s\n", SDL_GetError());
		success = false;
	}
	else {
		//Set tex filtering to enabled
		if (!SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "1"))
			printf("Warning: Linear texture filtering not enabled..\n");
		//Create window
		gWin = SDL_CreateWindow("SDL", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_W, SCREEN_H, SDL_WINDOW_SHOWN);
		if (gWin == NULL) {
			printf("Window could not be created! SDL Error: %s\n", SDL_GetError());
			success = false;
		}
		//Create vsynced renderer
		gRenderer = SDL_CreateRenderer(gWin, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
		if (gRenderer == NULL) {
			printf("Renderer could not be created! SDL Error: %s\n", SDL_GetError());
			success = false;
		}
		else {
			//Init renderer color
			SDL_SetRenderDrawColor(gRenderer, 0xFF, 0xFF, 0xFF, 0xFF);
			//Init PNG loading
			int imgFlags = IMG_INIT_PNG;
			if (!(IMG_Init(imgFlags) & imgFlags)) {
				printf("SDL_image could not be initialized! SDL_image Error: %s\n", IMG_GetError());
				success = false;
			}
		}
	} return success;
}

bool loadMedia() {
	//Flag
	bool success = true;
	//Load tex
	if (!gDotTex.loadFromFile("C:/Users/ricar/libgdx-projs/FlappyB/desktop/build/resources/main/bird.png")) {
		//if (!gDotTex.loadFromFile("C:/Users/ricar/Downloads/31_scrolling_backgrounds/dot.bmp")) {
		printf("Failed to load dot texture..\n");
		success = false;
	}
	if (!gBckgTex.loadFromFile("C:/Users/ricar/libgdx-projs/FlappyB/desktop/build/resources/main/bg1.png")) {
		printf("Failed to load background texture..\n");
		success = false;
	}
	if (!gFloorTex.loadFromFile("C:/Users/ricar/libgdx-projs/FlappyB/desktop/build/resources/main/ground1.png")) {
		printf("Failed to load floor texture..\n");
		success = false;
	}
	//Load font texture
	if (!gBitmapFont.buildFont("C:/Users/ricar/Downloads/41_bitmap_fonts/lazyfont.png"))
	{
		printf("Failed to load bitmap font!\n");
		success = false;
	}

	//Load sprite sheet texture
	if (!gSpriteSheetTexture.loadFromFile("C:/Users/ricar/Pictures/birdanimation.png"))
	{
		printf("Failed to load walking animation texture!\n");
		success = false;
	}
	else
	{
		//Set sprite clips
		gSpriteClips[0].x = 0;
		gSpriteClips[0].y = 0;
		gSpriteClips[0].w = 34;
		gSpriteClips[0].h = 24;

		gSpriteClips[1].x = 34;
		gSpriteClips[1].y = 0;
		gSpriteClips[1].w = 34;
		gSpriteClips[1].h = 24;

		gSpriteClips[2].x = 68;
		gSpriteClips[2].y = 0;
		gSpriteClips[2].w = 34;
		gSpriteClips[2].h = 24;
	}

	return success;
}

void close() {
	//Free loaded images
	gSpriteSheetTexture.free();
	//Free textures and fonts
	gDotTex.free();
	gBckgTex.free();
	gFloorTex.free();
	gBitmapFont.free();
	//Destroy SDL components
	SDL_DestroyRenderer(gRenderer);
	SDL_DestroyWindow(gWin);
	gRenderer = NULL;
	gWin = NULL;
	//Quit SDL sub-systems
	IMG_Quit();
	SDL_Quit();
}

int main(int argc, char* args[]) {
	if (!init())
		printf("Failed to initialize!\n");
	else {
		if (!loadMedia())
			printf("Failed to load media files!");
		else {
			//Main loop
			bool quit = false;
			SDL_Event evt;
			Dot dot;
			int scrollingOffSet = 0;
			int frame = 0;

			while (!quit) {
				//Handle event on queue
				while (SDL_PollEvent(&evt) != 0) {
					if (evt.type == SDL_QUIT)
						quit = true;
					dot.handleEvent(evt);
				}
				//Update dot pos
				dot.move();
				//Scroll bckg
				--scrollingOffSet;
				if (scrollingOffSet < -gBckgTex.getWidth())
					scrollingOffSet = 0;
				//Clear
				SDL_SetRenderDrawColor(gRenderer, 0xFF, 0xFF, 0xFF, 0xFF);
				SDL_RenderClear(gRenderer);
				//Render dot and background
				gBckgTex.render(scrollingOffSet, 0);
				gBckgTex.render(scrollingOffSet + gBckgTex.getWidth(), 0);
				gFloorTex.render(scrollingOffSet, 400);
				gFloorTex.render(scrollingOffSet + gFloorTex.getWidth(), 400);
				//Render current frame
				SDL_Rect* currentClip = &gSpriteClips[frame / 3];
				dot.render(currentClip);
				//gSpriteSheetTexture.render((SCREEN_W - currentClip->w) / 2, (SCREEN_H - currentClip->h) / 2, currentClip);
				//Render text
				int amount = SDL_GetTicks() / 1000;
				sprintf_s(time_msg, "Time: %d", amount);
				gBitmapFont.renderText(SCREEN_W - 90, 0, time_msg);
				//Update screen
				SDL_RenderPresent(gRenderer);
				//Go to next frame
				++frame;
				printf("%d\n", SDL_GetTicks()/1000);
				//Cycle animation
				if (frame / 3 >= WALKING_ANIMATION_FRAMES)
				{
					frame = 0;
				}
			}
		}
	}//Free res and close SDL
	close();
	return 0;
}
