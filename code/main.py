import pygame, sys, time, random
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
		self.current_session_score = 0
		self.start_offset = 0
		
		# quiz system
		self.quiz_mode = False
		self.current_question = 0
		self.questions = [
			{"question": "What are the pyramids of Giza made of?", "answers": ["Sandstone", "Limestone", "Granite"], "correct": 1},
			{"question": "Which civilization built Machu Picchu?", "answers": ["Aztec", "Inca", "Maya"], "correct": 1},
			{"question": "What is the study of ancient civilizations called?", "answers": ["Geology", "Archaeology", "Anthropology"], "correct": 1},
			{"question": "In which country is Petra located?", "answers": ["Egypt", "Jordan", "Syria"], "correct": 1},
			{"question": "What does a carbon dating method determine?", "answers": ["Size", "Age", "Weight"], "correct": 1},
			{"question": "Which ancient wonder was in Alexandria?", "answers": ["Lighthouse", "Garden", "Temple"], "correct": 0},
			{"question": "What tool do archaeologists use to carefully remove dirt?", "answers": ["Hammer", "Trowel", "Shovel"], "correct": 1},
			{"question": "Stonehenge is located in which country?", "answers": ["Ireland", "England", "Scotland"], "correct": 1},
			{"question": "What is a potsherd?", "answers": ["Broken pottery", "Stone tool", "Bone fragment"], "correct": 0},
			{"question": "The Rosetta Stone helped decode which language?", "answers": ["Latin", "Hieroglyphics", "Sanskrit"], "correct": 1},
			{"question": "What is stratigraphy in archaeology?", "answers": ["Dating method", "Layer study", "Tool making"], "correct": 1},
			{"question": "Which civilization created cuneiform writing?", "answers": ["Egyptian", "Sumerian", "Greek"], "correct": 1},
			{"question": "What is an artifact?", "answers": ["Natural rock", "Human-made object", "Animal bone"], "correct": 1},
			{"question": "Pompeii was destroyed by which volcano?", "answers": ["Etna", "Vesuvius", "Stromboli"], "correct": 1},
			{"question": "What does BCE stand for?", "answers": ["Before Common Era", "Before Christ Era", "British Colonial Era"], "correct": 0},
			{"question": "The Parthenon was built in which city?", "answers": ["Rome", "Athens", "Sparta"], "correct": 1},
			{"question": "What is the oldest known writing system?", "answers": ["Hieroglyphics", "Cuneiform", "Alphabet"], "correct": 1},
			{"question": "Which period came before the Bronze Age?", "answers": ["Iron Age", "Stone Age", "Modern Age"], "correct": 1},
			{"question": "What is a tell in archaeology?", "answers": ["Story", "Artificial mound", "Dating method"], "correct": 1},
			{"question": "Howard Carter discovered whose tomb?", "answers": ["Cleopatra", "Tutankhamun", "Ramesses"], "correct": 1},
			{"question": "What is provenance in archaeology?", "answers": ["Age of artifact", "Origin location", "Material type"], "correct": 1},
			{"question": "The Colosseum is in which city?", "answers": ["Athens", "Rome", "Naples"], "correct": 1},
			{"question": "What is paleontology?", "answers": ["Study of fossils", "Study of tools", "Study of buildings"], "correct": 0},
			{"question": "Which civilization built Angkor Wat?", "answers": ["Thai", "Khmer", "Vietnamese"], "correct": 1},
			{"question": "What is a midden?", "answers": ["Burial site", "Trash dump", "Water source"], "correct": 1},
			{"question": "The Terracotta Army is in which country?", "answers": ["Japan", "China", "Korea"], "correct": 1},
			{"question": "What is radiocarbon dating used for?", "answers": ["Metal artifacts", "Organic materials", "Stone tools"], "correct": 1},
			{"question": "Which ancient city was rediscovered in 1748?", "answers": ["Troy", "Pompeii", "Babylon"], "correct": 1},
			{"question": "What is a mummy?", "answers": ["Statue", "Preserved body", "Ancient book"], "correct": 1},
			{"question": "The Dead Sea Scrolls were found in which country?", "answers": ["Egypt", "Israel", "Jordan"], "correct": 1},
			{"question": "What is dendrochronology?", "answers": ["Tree ring dating", "Pottery study", "Bone analysis"], "correct": 0},
			{"question": "Which culture built Easter Island statues?", "answers": ["Polynesian", "Melanesian", "Micronesian"], "correct": 0},
			{"question": "What is an excavation grid used for?", "answers": ["Dating", "Recording location", "Measuring depth"], "correct": 1},
			{"question": "The Sphinx has the body of what animal?", "answers": ["Horse", "Lion", "Bull"], "correct": 1},
			{"question": "What is obsidian?", "answers": ["Metal", "Volcanic glass", "Clay"], "correct": 1},
			{"question": "Which empire built the Colosseum?", "answers": ["Greek", "Roman", "Byzantine"], "correct": 1},
			{"question": "What is a dolmen?", "answers": ["Stone table", "Grave marker", "Both A and B"], "correct": 2},
			{"question": "The Nazca Lines are in which country?", "answers": ["Chile", "Peru", "Bolivia"], "correct": 1},
			{"question": "What is thermoluminescence dating used for?", "answers": ["Wood", "Ceramics", "Metal"], "correct": 1},
			{"question": "Which pharaoh built the Great Pyramid?", "answers": ["Khafre", "Khufu", "Menkaure"], "correct": 1},
			{"question": "What is an amphora?", "answers": ["Weapon", "Storage jar", "Coin"], "correct": 1},
			{"question": "Çatalhöyük is an ancient site in which country?", "answers": ["Greece", "Turkey", "Iran"], "correct": 1},
			{"question": "What is a sarcophagus?", "answers": ["Temple", "Stone coffin", "Statue"], "correct": 1},
			{"question": "The Olmec civilization was in which region?", "answers": ["Peru", "Mexico", "Guatemala"], "correct": 1},
			{"question": "What is a cairn?", "answers": ["Stone pile", "Burial mound", "Both A and B"], "correct": 2},
			{"question": "Lascaux Cave paintings are in which country?", "answers": ["Spain", "France", "Italy"], "correct": 1},
			{"question": "What is a henge?", "answers": ["Stone circle", "Hill fort", "Burial chamber"], "correct": 0},
			{"question": "The Code of Hammurabi was written in which civilization?", "answers": ["Egyptian", "Babylonian", "Persian"], "correct": 1},
			{"question": "What is magnetic susceptibility used to detect?", "answers": ["Metal objects", "Hidden features", "Age of sites"], "correct": 1},
			{"question": "The Palace of Knossos was built by which civilization?", "answers": ["Mycenaean", "Minoan", "Greek"], "correct": 1}
		]
		
		# Shuffle the questions randomly at game start
		random.shuffle(self.questions)

		# menu
		self.menu_surf = pygame.image.load('../graphics/ui/menu.png').convert_alpha()
		self.menu_rect = self.menu_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 20))

		# music 
		self.music = pygame.mixer.Sound('../sounds/music.wav')
		self.music.play(loops = -1)

	def collisions(self):
		if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask)\
		or self.plane.rect.top <= 0:
			for sprite in self.collision_sprites.sprites():
				if sprite.sprite_type == 'obstacle':
					sprite.kill()
			# Freeze the current session score when collision happens
			self.current_session_score = (pygame.time.get_ticks() - self.start_offset) // 1000
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
		
	def wrap_text(self, text, font, max_width):
		"""Wrap text to fit within max_width pixels"""
		words = text.split(' ')
		lines = []
		current_line = []
		
		for word in words:
			# Test if adding this word would exceed max width
			test_line = ' '.join(current_line + [word])
			test_width = font.size(test_line)[0]
			
			if test_width <= max_width:
				current_line.append(word)
			else:
				# If current_line is empty, the word itself is too long
				if current_line:
					lines.append(' '.join(current_line))
					current_line = [word]
				else:
					lines.append(word)  # Add the long word anyway
					current_line = []
		
		# Add any remaining words
		if current_line:
			lines.append(' '.join(current_line))
		
		return lines
	
	def display_quiz(self):
		# Display current total score (frozen during quiz)
		total_score = self.accumulated_score + self.current_session_score
		score_text = f"Total Score: {total_score}"
		score_surf = self.font.render(score_text, True, 'blue')
		score_rect = score_surf.get_rect(center=(WINDOW_WIDTH / 2, 50))
		self.display_surface.blit(score_surf, score_rect)
		
		# Display question with word wrapping
		question_data = self.questions[self.current_question % len(self.questions)]
		question_text = question_data["question"]
		
		# Wrap the question text to fit within 80% of window width
		max_question_width = int(WINDOW_WIDTH * 0.8)
		question_lines = self.wrap_text(question_text, self.small_font, max_question_width)
		
		# Display each line of the wrapped question
		start_y = 130
		line_spacing = 25
		for i, line in enumerate(question_lines):
			question_surf = self.small_font.render(line, True, 'brown')
			question_rect = question_surf.get_rect(center=(WINDOW_WIDTH / 2, start_y + i * line_spacing))
			self.display_surface.blit(question_surf, question_rect)
		
		# Display answer options
		# Adjust answer position based on number of question lines
		answer_start_y = start_y + len(question_lines) * line_spacing + 20
		for i, answer in enumerate(question_data["answers"]):
			color = 'brown' if i == question_data["correct"] else 'brown'
			answer_text = f"{i + 1}. {answer}"
			answer_surf = self.small_font.render(answer_text, True, color)
			answer_rect = answer_surf.get_rect(center=(WINDOW_WIDTH / 2, answer_start_y + i * 30))
			self.display_surface.blit(answer_surf, answer_rect)
		
		# Display instructions
		instruction_y = answer_start_y + 3 * 30 + 20
		instruction_surf = self.small_font.render("Press 1, 2, or 3 to answer!", True, 'blue')
		instruction_rect = instruction_surf.get_rect(center=(WINDOW_WIDTH / 2, instruction_y))
		self.display_surface.blit(instruction_surf, instruction_rect)
		
	def handle_quiz_answer(self, answer_index):
		question_data = self.questions[self.current_question % len(self.questions)]
		if answer_index == question_data["correct"]:
			# Correct answer - continue playing with accumulated score
			self.accumulated_score += self.current_session_score
			self.current_session_score = 0
			self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
			self.active = True
			self.quiz_mode = False
			self.start_offset = pygame.time.get_ticks()
			self.current_question += 1
		else:
			# Wrong answer - reset everything
			self.accumulated_score = 0
			self.current_session_score = 0
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