#include <SDL.h>
#include <SDL_image.h>
#include <stdio.h>
#include <string>

const static int SCREEN_W = 640, SCREEN_H = 480;

class LTexture {
public:
	LTexture();
	~LTexture();
	bool loadFromFile(std::string path);
	void free();
	//Sets
	void setColor(Uint8 r, Uint8 g, Uint8 b);
	void setBlendMode(SDL_BlendMode blending);
	void setAlpha(Uint8 alpha);
	void render(int x, int y, SDL_Rect* clip = NULL, double ang = 0.0, SDL_Point* center = NULL, SDL_RendererFlip flip = SDL_FLIP_NONE);
	//Gets
	int getWidth();
	int getHeight();
private:
	SDL_Texture* mTex;
	int m_w, m_h;
};

class Dot {
public:
	static const int DOT_W = 15, DOT_H = 15, DOT_VEL = 4;
	Dot();
	void handleEvent(SDL_Event& evt);
	void move();
	void render();
private:
	int mPosX, mPosY, mVelX, mVelY;
};
//Methods
bool init();
bool loadMedia();
void close();
//Vars
SDL_Window* gWin = NULL;
SDL_Renderer* gRenderer = NULL;
LTexture gDotTex, gBckgTex, gFloorTex;

LTexture::LTexture() {
	//Constructor
	mTex = NULL;
	m_w = 0;
	m_h = 0;
}

LTexture::~LTexture() {
	free();
}

bool LTexture::loadFromFile(std::string path) {
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
}

void LTexture::free() {
	//Clear tex
	if (mTex != NULL) {
		SDL_DestroyTexture(mTex);
		mTex = NULL;
		m_w = 0;
		m_h = 0;
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

void Dot::render() {
	gDotTex.render(mPosX, mPosY);
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
	return success;
}

void close() {
	//Free textures
	gDotTex.free();
	gBckgTex.free();
	gFloorTex.free();
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
				dot.render();
				//Update screen
				SDL_RenderPresent(gRenderer);
			}
		}
	}//Free res and close SDL
	close();
	return 0;
}
