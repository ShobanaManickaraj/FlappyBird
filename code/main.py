import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle

class Game:
	def __init__(self):
		
		# setup
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption('Flappy Bird')
		self.clock = pygame.time.Clock()
		self.active = True

		# sprite groups
		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()

		# scale factor
		bg_height = pygame.image.load('../graphics/environment/background.png').get_height()
		self.scale_factor = WINDOW_HEIGHT / bg_height

		# sprite setup 
		BG(self.all_sprites,self.scale_factor)
		Ground([self.all_sprites,self.collision_sprites],self.scale_factor)
		self.plane = Plane(self.all_sprites,self.scale_factor / 1.7)

		# timer
		self.obstacle_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.obstacle_timer,1400)

		# text
		self.font = pygame.font.Font('../graphics/font/BD_Cartoon_Shout.ttf',30)
		self.small_font = pygame.font.Font('../graphics/font/BD_Cartoon_Shout.ttf',20)
		self.score = 0
		self.accumulated_score = 0
		self.start_offset = 0
		
		# quiz system
		self.quiz_mode = False
		self.current_question = 0
		self.questions = [
			{"question": "What is 2 + 2?", "answers": ["3", "4", "5"], "correct": 1},
			{"question": "What color is the sky?", "answers": ["Blue", "Red", "Green"], "correct": 0},
			{"question": "How many legs does a spider have?", "answers": ["6", "8", "10"], "correct": 1},
			{"question": "What is the capital of France?", "answers": ["London", "Paris", "Rome"], "correct": 1},
			{"question": "How many days in a week?", "answers": ["5", "6", "7"], "correct": 2}
		]

		# menu
		self.menu_surf = pygame.image.load('../graphics/ui/menu.png').convert_alpha()
		self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2))

		# music 
		self.music = pygame.mixer.Sound('../sounds/music.wav')
		self.music.play(loops = -1)

	def collisions(self):
		if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask)\
		or self.plane.rect.top <= 0:
			for sprite in self.collision_sprites.sprites():
				if sprite.sprite_type == 'obstacle':
					sprite.kill()
			self.active = False
			self.quiz_mode = True
			self.plane.kill()

	def display_score(self):
		if self.active:
			self.score = (pygame.time.get_ticks() - self.start_offset) // 1000 + self.accumulated_score
			y = WINDOW_HEIGHT / 10
		else:
			if self.quiz_mode:
				self.display_quiz()
				return
			y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

		score_surf = self.font.render(str(self.score),True,'black')
		score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2,y))
		self.display_surface.blit(score_surf,score_rect)
		
	def display_quiz(self):
		# Display current total score
		total_score = self.accumulated_score + ((pygame.time.get_ticks() - self.start_offset) // 1000 if hasattr(self, 'start_offset') else 0)
		score_text = f"Total Score: {total_score}"
		score_surf = self.font.render(score_text, True, 'white')
		score_rect = score_surf.get_rect(center=(WINDOW_WIDTH / 2, 50))
		self.display_surface.blit(score_surf, score_rect)
		
		# Display question
		question_data = self.questions[self.current_question % len(self.questions)]
		question_surf = self.small_font.render(question_data["question"], True, 'white')
		question_rect = question_surf.get_rect(center=(WINDOW_WIDTH / 2, 150))
		self.display_surface.blit(question_surf, question_rect)
		
		# Display answer options
		for i, answer in enumerate(question_data["answers"]):
			color = 'yellow' if i == question_data["correct"] else 'white'
			answer_text = f"{i + 1}. {answer}"
			answer_surf = self.small_font.render(answer_text, True, color)
			answer_rect = answer_surf.get_rect(center=(WINDOW_WIDTH / 2, 200 + i * 40))
			self.display_surface.blit(answer_surf, answer_rect)
		
		# Display instructions
		instruction_surf = self.small_font.render("Press 1, 2, or 3 to answer!", True, 'cyan')
		instruction_rect = instruction_surf.get_rect(center=(WINDOW_WIDTH / 2, 350))
		self.display_surface.blit(instruction_surf, instruction_rect)
		
	def handle_quiz_answer(self, answer_index):
		question_data = self.questions[self.current_question % len(self.questions)]
		if answer_index == question_data["correct"]:
			# Correct answer - continue playing with accumulated score
			self.accumulated_score += (pygame.time.get_ticks() - self.start_offset) // 1000
			self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
			self.active = True
			self.quiz_mode = False
			self.start_offset = pygame.time.get_ticks()
			self.current_question += 1
		else:
			# Wrong answer - reset everything
			self.accumulated_score = 0
			self.current_question = 0
			self.quiz_mode = False
			# Stay in game over state

	def run(self):
		last_time = time.time()
		while True:
			
			# delta time
			dt = time.time() - last_time
			last_time = time.time()

			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if self.quiz_mode:
						if event.key == pygame.K_1:
							self.handle_quiz_answer(0)
						elif event.key == pygame.K_2:
							self.handle_quiz_answer(1)
						elif event.key == pygame.K_3:
							self.handle_quiz_answer(2)
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.active:
						self.plane.jump()
					elif not self.quiz_mode:
						self.plane = Plane(self.all_sprites,self.scale_factor / 1.7)
						self.active = True
						self.start_offset = pygame.time.get_ticks()

				if event.type == self.obstacle_timer and self.active:
					Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)
			
			# game logic
			self.display_surface.fill('black')
			self.all_sprites.update(dt)
			self.all_sprites.draw(self.display_surface)
			self.display_score()

			if self.active: 
				self.collisions()
			else:
				self.display_surface.blit(self.menu_surf,self.menu_rect)

			pygame.display.update()
			# self.clock.tick(FRAMERATE)

if __name__ == '__main__':
	game = Game()
	game.run()