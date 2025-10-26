-- Extra seed data: short, medium, long, and noisy examples

-- ===== POSITIVE =====
INSERT INTO training_samples (text_raw, label) VALUES
-- short
('Amazing!', 'pos'),
('Loved it.', 'pos'),
('Nice!', 'pos'),
('Wow', 'pos'),

-- medium
('The sushi was fresh and perfectly seasoned.', 'pos'),
('Great ambience and friendly staff made our night perfect.', 'pos'),
('Clean room, comfy bed, and quick check-in.', 'pos'),
('Delivery arrived early, everything still warm and tasty.', 'pos'),

-- long
('From the moment we arrived until checkout, everything was smooth. The staff went out of their way to accommodate us, \
even offering a late breakfast when we overslept. Definitely coming back!', 'pos'),
('I had doubts after reading mixed reviews, but honestly this was one of the best experiences I have had in months. \
Food, service, and even the playlist were spot on. Worth every penny.', 'pos'),

-- noisy / informal
('yesss!!! soooo good omg 🔥🔥🔥', 'pos'),
('10/10 will buy again!!! lol', 'pos'),
('luv the app interface, super ez 2 use 👍', 'pos'),
('Gr8 taste! no cap 😋', 'pos');

-- ===== NEGATIVE =====
INSERT INTO training_samples (text_raw, label) VALUES
-- short
('Bad.', 'neg'),
('Ugh.', 'neg'),
('Nope', 'neg'),

-- medium
('Slow service and cold food, disappointing.', 'neg'),
('App keeps crashing after login, unusable.', 'neg'),
('Rude staff ruined an otherwise nice place.', 'neg'),
('Overpriced for the quality provided.', 'neg'),

-- long
('We waited nearly an hour for our order and when it finally arrived half of it was missing. \
The manager apologized but offered nothing to make up for it. Definitely not returning.', 'neg'),
('The first few months were fine, but lately the quality has dropped drastically. \
Support takes forever to respond and shipments arrive late. Very frustrating.', 'neg'),

-- noisy / informal
('wtf this was trash 😡😡😡', 'neg'),
('nah bruh, totally mid 😒', 'neg'),
('spam emails every day!!! STOP!!!', 'neg'),
('ehh idk it just doesnt hit the same anymore lol', 'neg');
