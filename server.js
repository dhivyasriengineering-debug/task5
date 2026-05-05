const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

const app = express();
app.use(express.json());

const PORT = 3000;
const JWT_SECRET = "your_secret_key";

// fake database
const users = [];

// REGISTER
app.post('/register', async (req, res) => {
  const { username, password } = req.body;

  const hashedPassword = await bcrypt.hash(password, 10);

  users.push({
    username,
    password: hashedPassword
  });

  res.send("User registered");
  
});

// LOGIN
app.post('/login', async (req, res) => {
  const { username, password } = req.body;

  const user = users.find(u => u.username === username);
  if (!user) return res.status(401).send("User not found");

  const valid = await bcrypt.compare(password, user.password);
  if (!valid) return res.status(401).send("Invalid password");

  const token = jwt.sign(
    { username: user.username },
    JWT_SECRET,
    { expiresIn: "1h" }
  );

  res.json({ token });
});

// Middleware
function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader) return res.status(401).send("No token provided");

  const token = authHeader.split(" ")[1];

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch {
    res.status(401).send("Invalid token");
  }
}

// Protected route
app.get('/protected', authMiddleware, (req, res) => {
  res.send(`Welcome ${req.user.username}, you have access!`);
});

// HOME TEST ROUTE
app.get('/', (req, res) => {
  res.send("API is working");
});

// START SERVER (ONLY ONCE)
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
app.use(express.json()); 
app.use(express.urlencoded({ extended: true }));