class AutomateTwitch(AutomateType):

	total_watch_time = 0

	def __init__(self, auto_parent, driver, configuration, lock):
		super().__init__(auto_parent, driver, configuration, lock)

	def start_time_delay(self):

		record_time = 1800 # time in seconds
		timer = time.time()
		while time.time() - timer < record_time: # time in seconds

			max_limit = 3 # seconds to wait for start time delay
			i = 0
			# array of videos that the screen sees
			videos = self.driver.find_elements(By.XPATH, '//android.widget.FrameLayout[contains(@resource-id, "left_container")]')
			
			while i < len(videos):
				
				start_time = 0
				flag = False
				loop_time = time.time()
				videos[i].click()
				while time.time() - loop_time < max_limit:
					delay_sign = self.driver.find_elements(By.XPATH, '//android.widget.ProgressBar[@class="android.widget.ProgressBar"]')
					
					if len(delay_sign) != 0:
						get_time = time.time() # "start-time" begin
						flag = True
						logging.info("[[MSG]]Begin start time")

					while len(delay_sign) != 0:  # while delay is active, get the element while is present
						delay_sign = self.driver.find_elements(By.XPATH, '//android.widget.ProgressBar[@class="android.widget.ProgressBar"]')
					if flag:
						start_time = time.time() - get_time # "start-time" end
						logging.info("[[MSG]]End start time, Value is: {}".format(start_time))
						self.driver.press_keycode(4) # back button
						sleep(2)

				if not flag:
					self.driver.press_keycode(4) # back button
					sleep(2)
				i+=1
				if time.time() - timer >= record_time:
					print("finished")
					return

			self.swipe(470, 2000, 470, 500, 600, 1)

		print("finished")
		self.driver.press_keycode(3)
			
	def set_quality(self, quality):

		# [1272,84][1440,252] is the settings button coordinates (always same place top right)
		self.driver.tap([('1356','168')])
		sleep(3)
		apply = self.driver.find_elements(By.ID, 'tv.twitch.android.app:id/confirm_changes_button')

		if len(apply) == 0:
			return -1
		
		status = self.click('XPath', '//android.widget.TextView[@text="{}"]'.format(quality), desc=" on quality: {}".format(quality)) # click on quality
		sleep(1)
		apply[0].click()  # click on apply changes (purple button)
		return status

	def quality_stalling(self, quality): # take from here

		record_time = 3600 # time in seconds
		while self.total_watch_time < record_time: # time in seconds

			i = 0 # for videos
			j = 0 # for times
			fix = 0

			videos = self.driver.find_elements(By.XPATH, '//android.widget.FrameLayout[contains(@resource-id, "left_container")]')  # array of the n videos that the screen sees
			times = self.driver.find_elements(By.XPATH, '//android.widget.TextView[contains(@resource-id, "live_text")]')  # array of the n video times the screen sees

			if len(videos) != len(times): # if i can see video but not the time before click, dont even try to work with it.
				i = 1
				fix = 1

			attempt_fix_count = 0
			while i < len(videos) - fix:  # 'i' is number of video from what the screen can see

				str_time = self.get_time(times[j])

				print("time for video: " + str(i) + " is " + str(str_time) + "s")
				videos[i].click()
				sleep(1)
				status = self.set_quality(quality)

				if status == 0: # if quality does not exist move on to next vid
					print("skipping video with unwanted quality")
					self.driver.press_keycode(4)  # not always working
					check = self.driver.find_elements(By.XPATH, '//android.widget.TextView[@text="Chat Replay"]')
					while len(check) > 0:
						print("applying fix")
						self.driver.press_keycode(4)  # not always working
						sleep(1)
						check = self.driver.find_elements(By.XPATH, '//android.widget.TextView[@text="Chat Replay"]')
					sleep(1)
					i+=1
					j+=1
					attempt_fix_count = 0
					continue

				elif status == -1: # cant click the settings button, trying again
					print("trying to press settings again")
					attempt_fix_count += 1
					self.driver.press_keycode(4)
					if attempt_fix_count > 5: # fixes "video is not available problem"
						i+=1
						j+=1
						attempt_fix_count = 0
					print(attempt_fix_count)
					check = self.driver.find_elements(By.XPATH, '//android.widget.TextView[@text="Chat Replay"]')
					while len(check) > 0:
						print("applying fix")
						self.driver.press_keycode(4)  # not always working
						sleep(1)
						check = self.driver.find_elements(By.XPATH, '//android.widget.TextView[@text="Chat Replay"]')
					continue

				elif status == 1:
					attempt_fix_count = 0

				timer = str_time*0.6  # watch up to 60% of the video
				stall = False
				stall_duration = 0
				time_passed = time.time() # start of time counter for current video
				logging.info("[[MSG]]Begin video")

				# inside the infinit video loop which stoppes after timer
				while True:

					if (time.time() - time_passed > timer) or ((self.total_watch_time + (time.time() - time_passed)) > record_time):
						break
					
					delay_sign = self.driver.find_elements(By.XPATH, '//android.widget.ProgressBar[@class="android.widget.ProgressBar"]')
					if len(delay_sign) != 0:
						stall = True
						logging.info("[[MSG]]Start stall")
						get_time = time.time()
					
					while len(delay_sign) != 0:  # while delay is active, get the element while is present
						delay_sign = self.driver.find_elements(By.XPATH, '//android.widget.ProgressBar[@class="android.widget.ProgressBar"]')
						stall_duration = time.time() - get_time
					
					if stall:
						logging.info("[[MSG]]End stall, duration: {}".format(stall_duration))
						stall = False
					
				self.total_watch_time += (time.time() - time_passed)
				print("watched until now: " + str(self.total_watch_time) + "s from total of wanted: " + str(record_time) + "s")
				logging.info("[[MSG]]End video")

				if self.total_watch_time > record_time:
					print("pressing home button")
					print("finished")
					self.driver.press_keycode(3)
					return

				print("pressing back")
				self.driver.press_keycode(4)
				sleep(0.5)
				i+=1
				j+=1

			sleep(2) # wait for video to exit and then swipe
			self.swipe(470, 2000, 470, 500, 600, 1)

		print("finished")

	def screen_click(self):
		screen = self.driver.find_elements(By.ID, 'tv.twitch.android.app:id/playback_view_container')
		while (len(screen) == 0):
			screen = self.driver.find_elements(By.ID, 'tv.twitch.android.app:id/playback_view_container')
		screen[0].click()


	def get_time(self, time_obj):

		str_time = time_obj.get_attribute('text')
		time_arr = str_time.split(':')
		
		if len(time_arr) == 1:   # seconds
			return int(time_arr[0])

		elif len(time_arr) == 2: # minuts + seconds
			return int(time_arr[0])*60 + int(time_arr[1])

		elif len(time_arr) == 3: # hours + minuts + seconds
			return int(time_arr[0])*3600 + int(time_arr[1])*60 + int(time_arr[2])

	def test(self):

		check = self.driver.press_keycode(4)
		if check is not None:
			print("backed out")

class AutomateFacebook(AutomateType):

	start_times = []
	vid_len = 0

	def __init__(self, auto_parent, driver, configuration, lock):
		super().__init__(auto_parent, driver, configuration, lock)

	def login(self,username,password):
		self.lock.acquire()
		try:
			username = self.driver.find_elements_by_accessibility_id('Username');
			password = self.driver.find_elements_by_accessibility_id('Password');

			if len(username)>0 and len(password)>0:
				username[0].set_value(username)
				password[0].set_value(password)
				login = self.driver.find_elements_by_accessibility_id('Log In')[0];
				login.click()
				sleep(6)
				
			ok = self.driver.find_elements(By.XPATH, '//android.widget.Button[@text="OK"]')
			if len(ok)>0:
				ok[0].click()
			sleep(5)
			deny = self.driver.find_elements_by_accessibility_id('Deny')
			while len(deny)>0:
				print("Clicked Deny button")
				deny[0].click()
				sleep(2)
				deny = self.driver.find_elements_by_accessibility_id('Deny')
		finally:
			self.lock.release()

	def open(self):
		super().open('com.facebook.katana/com.facebook.katana.activity.FbMainTabActivity')

	def clear_cache(self):
		super().clear_cache('com.facebook.katana') # phone needs to be rooted for this action to work

	def vid_click(self):
		print("clicking on video player")
		try:
			screenElement = self.driver.find_elements(By.XPATH, '(//android.view.ViewGroup[@content-desc="Video"])[1]')
			while len(screenElement) == 0:
				screenElement = self.driver.find_elements(By.XPATH, '(//android.view.ViewGroup[@content-desc="Video"])[1]')
			screenElement[0].click()
		except:
			pass
			self.swipe(470, 2000, 470, 2500, 600, 2)
			self.vid_click()

	# reset video to start
	def move_seekbar(self):
		
		print("reseting the buffer to 0")
		sleep(0.5)
		try:
			seekbar_elem = self.driver.find_element_by_class_name('android.widget.SeekBar')
			while seekbar_elem is None:
				seekbar_elem = self.driver.find_element_by_class_name('android.widget.SeekBar')
			start_x = seekbar_elem.location.get('x')
			start_y = seekbar_elem.location.get('y')
			self.driver.tap([(start_x,start_y)])
		except:
			pass


# 	get screen elements from array of possible xpath's
	def get_screen_elem(self, arr):
		i = 0
		arr_len = len(arr)
		screenElement = self.driver.find_elements(By.XPATH, arr[i])
		for k in range(arr_len-1):
			if len(screenElement) != 0:
				break
			i+=1
			screenElement = self.driver.find_elements(By.XPATH, arr[i])
		
		return screenElement

	# for playlists of 12 videos
	def start_time_delay(self):  # copy
		
		second_half = False
		i=0
		
		videos = self.driver.find_elements(By.XPATH, '//android.view.View[@index="0"]')  # array of the 6 videos that the screen sees
		while i != 7:

			start_time = 0
			videos[i].click()
			max_limit = 5
			flag = False
			loop_time = time.time()
			self.lock.acquire()
			while time.time() - loop_time < max_limit:
				
				delay_sign = self.driver.find_elements(By.XPATH, '//android.widget.ProgressBar[@class="android.widget.ProgressBar"]')

				if len(delay_sign) != 0:
					get_time = time.time()
					flag = True
					logging.info("[[MSG]]Begin start time")

				while len(delay_sign) != 0:  # while delay is active, get the element while is present
					delay_sign = self.driver.find_elements(By.XPATH, '//android.widget.ProgressBar[@class="android.widget.ProgressBar"]')
				
				if flag:
					start_time = time.time() - get_time
					logging.info("[[MSG]]End start time, Value is: {}".format(start_time))
					self.driver.press_keycode(4)
					sleep(3)

			if not flag:
				self.driver.press_keycode(4)
				sleep(3)
			self.lock.release()
			i+=1

			if (i % 6) == 0 and not second_half:
				self.swipe(470, 2000, 470, 0, 600, 1)
				sleep(3)
				videos = self.driver.find_elements(By.XPATH, '//android.view.View[@index="0"]')
				i = 1
				second_half = True


	# returns end time of video buffer, also good for clicking the video
	def click_and_time(self):

		time = None
		first_screen_opt = ['//android.widget.RelativeLayout[@content-desc="video player"]','(//android.view.ViewGroup[@content-desc="Video"])[1]']
		second_screen_opt = ['(//android.widget.RelativeLayout[@content-desc="video player"])[2]','(//android.view.ViewGroup[@content-desc="Video"])[2]']
		iterations = -1
		while time is None:

			first_screenElement = self.get_screen_elem(first_screen_opt)
			secondScreen_element = self.get_screen_elem(second_screen_opt)

			if len(first_screenElement)>0 and len(secondScreen_element)>0:
				print("clicking on first video screen")
				self.lock.acquire()
				first_screenElement[0].click()
				self.lock.release()
				sleep(0.5)

			elif len(first_screenElement)>0:
				print("clicking on first video screen from else")
				self.lock.acquire()
				first_screenElement[0].click()
				self.lock.release()
				sleep(0.5)

			else:
				print("can't click on screen, som't is blocking")
				return 1

			time = self.get_field('XPath', '//android.widget.TextView[(@index="2") and not (@text="Share")]')
			iterations += 1

			if iterations >= 4:
				self.swipe(470, 2000, 470, 2500, 600, 2)
				sleep(1)
				self.swipe(470, 2000, 470, 2500, 600, 2)
				sleep(1)
				iterations = 0

		return time

	# options = [144p, 180p 240, 270p, 360p, 480p, 640p, 720p, 840p 1080p]  TODO: add functionsality to work with what needed
	def set_quality(self, quality):
		success = 0
		while success == 0:
			success = self.click('XPath', '//android.widget.ImageView[@content-desc="Video Quality"]', desc=" on quality")
			sleep(0.5)
			success = self.click('XPath', '//android.widget.Button[@content-desc="{}"]'.format(quality), desc=" on quality: {}".format(quality))
			print("succsess is: " + str(success))
			if success == 0:
				check = self.click_and_time()
				sleep(0.5)
				if check == 1:
					self.driver.press_keycode(4)
					sleep(0.5)
					self.driver.press_keycode(4)
					return 1

		self.driver.press_keycode(4)
		return 0

	def play(self):
		play = self.driver.find_elements(By.XPATH, '//android.widget.ImageButton[@content-desc="Play current video"]')
		if len(play)>0:
			print("play is active")
			play[0].click()
			
		
	# this func is for:
	# 1. restoring the buffer to 0 from end.
	# 2. start the video from start even if didn't have enough time for (1).
	# 3. fixes event when "facebook desides" not to give the quality list and gives only "auto" option,
	#    basically it tries to go back and work with the same video again, if doesn't help, continues to the
	#    next video if exists.
	def fix_facebook_set_quality(self, quality, videos, idx, limit):

		quality_prob_times = 0

		self.vid_click()
		self.move_seekbar()
		sleep(4)
		self.vid_click()
		self.move_seekbar()
		sleep(15)
		self.swipe(470, 2000, 470, 2500, 600, 2)
		sleep(1)
		self.swipe(470, 2000, 470, 2500, 600, 2)
		self.vid_click()
		self.move_seekbar()
		sleep(4)
		check = self.set_quality(quality)
		if check == 1 and quality_prob_times < 1:
			videos[idx].click()
			sleep(0.5)
			self.move_seekbar()
			sleep(15)
			self.swipe(470, 2000, 470, 2500, 600, 2)
			self.move_seekbar()
			sleep(4)
			check = self.set_quality(quality)
			# if doing it again didnt help, get out and move on to next vid if exists.
			if check == 1:
				quality_prob_times +=1

		if quality_prob_times == 1:
			if idx+1 != limit:
				idx+=1
				videos[idx].click()
				idx = self.fix_facebook_set_quality(quality, videos, idx, limit)
			else:
				return -1
		sleep(0.5)
		self.play()
		return idx

	def quality_stalling(self, quality):
		
		i = 0
		done = False
		max_vids = 7
		videos = self.driver.find_elements(By.XPATH, '//android.view.View[@index="0"]')  # array of the n videos that the screen sees
		
		while i != max_vids:  # 'i' is number of video from what the screen can see, max_vids is +1 (needed as a fix for after the scroll)

			vid_time_obj = None
			keep_watching = True
			stall = False
			stall_duration = 0
			end_time = 0   # value of time left from video buffer
			quality_prob_times = 0
			videos[i].click()
			i = self.fix_facebook_set_quality(quality, videos, i, max_vids)
			if i == -1:
				print("finished")
				return

			time_counter = time.time()
			set_time = 60
			logging.info("[[MSG]]Begin video")
			while keep_watching:

				self.play()
				if time.time() - time_counter >= set_time:  # at first check every minut, when the time comes after 10 sec
					retry = 0
					while retry == 0:
						try:
							vid_time_obj = self.click_and_time()
							vid_time_str = vid_time_obj.get_attribute('text')
							retry = 1
						except:
							pass
							vid_time_obj = self.click_and_time()
							vid_time_str = vid_time_obj.get_attribute('text')

					print("end time is: " + str(vid_time_str))
					arr = vid_time_str.split(':')
					end_time = int(arr[0][1])*60 + int(arr[1])
					print("time left: " + str(end_time) +"s")
					time_counter = time.time()
					if end_time <= 120:
						if end_time >= 60:
							set_time = 40
						else:
							set_time = 10
					if end_time <= 20:
						keep_watching = False
				
				delay_sign = self.driver.find_elements(By.XPATH, '//android.widget.ProgressBar[@class="android.widget.ProgressBar"]')
				if len(delay_sign) != 0:
					stall = True
					stall_id = get_new_id()
					logging.info("[[MSG]]Start stall")

				get_time = time.time()
				while len(delay_sign) != 0:  # while delay is active, get the element while is present
					self.lock.acquire()
					delay_sign = self.driver.find_elements(By.XPATH, '//android.widget.ProgressBar[@class="android.widget.ProgressBar"]')
					stall_duration = time.time() - get_time
					self.lock.release()
				
				if stall:
					logging.info("[[MSG]]End stall, duration: {}".format(stall_duration))
					stall = False
				
			logging.info("[[MSG]]End video")
			self.driver.press_keycode(4)
			sleep(0.5)

			i+=1

			if (i % 6) == 0 and not done:
				self.swipe(470, 2000, 470, 0, 600, 2)
				sleep(3)
				videos = self.driver.find_elements(By.XPATH, '//android.view.View[@index="0"]')
				if len(videos) == 8:
					max_vids = 8
					i = 2
				elif len(videos) == 7: # max_vids is already 7 so don't need to change it.
					i = 1
				done = True

		print("finished")

	