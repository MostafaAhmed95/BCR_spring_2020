from gym.envs.registration import register
#just add Bullet word in the id 
# also added Bullet word in the entry point 
register(id='dribblebotBullet-v0', entry_point='dribble_bot.envs:DribblebotBulletEnv',)