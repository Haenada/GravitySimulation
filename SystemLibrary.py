#!/usr/bin/env python
# coding: utf-8

# In[1]:


class CelestialObject():
    def __init__(self, name, mass, loc, velocity):
        self.name = name 
        self.mass = mass #kg
        self.loc = loc # km (3 length list x,y,z)
        self.velocity = velocity  #km/s (3 length list x,y,z)
        
def basicSolarSystem():
    from astropy import units as u
    from astropy.constants import M_sun
    Sun = CelestialObject("Sol", M_sun.value, [0, 0, 0], [0, 0, 0])
    Mercury = CelestialObject("Mercury", 3.3*(10**23), 
                              [(0.3075*u.au).to(u.km).value, 0, 0], [0, 47.9, 0])
    Venus = CelestialObject("Venus", 4.9*(10**24), 
                            [(0.7184*u.au).to(u.km).value, 0, 0], [0, 35, 0])
    Earth = CelestialObject("Earth", 6.0*(10**24), 
                            [(1*u.au).to(u.km).value, 0, 0], [0, 29.8, 0])
    Mars = CelestialObject("Mars", 6.4*(10**23),
                           [(1.382*u.au).to(u.km).value, 0, 0], [0, 24.1, 0])
    Jupyter = CelestialObject("Jupyter", 1.898*(10**27), 
                              [(4.9501*u.au).to(u.km).value, 0, 0], [0, 13.1, 0])
    Saturn = CelestialObject("Saturn", 5.68*(10**26),
                             [(9.0412*u.au).to(u.km).value, 0, 0], [0, 9.7, 0])
    Uranus = CelestialObject("Uranus", 8.68*(10**25),
                             [(18.286*u.au).to(u.km).value, 0, 0], [0, 6.8, 0])
    Neptune = CelestialObject("Neptune", 1.024*(10**26),
                              [(29.81*u.au).to(u.km).value, 0, 0], [0, 5.4, 0])
    return [Sun, Mercury, Venus, Earth, Mars, Jupyter, Saturn, Uranus, Neptune]


# In[ ]:




