// @title           Course System Backend
// @version         1.0
// @description     API server for managing courses and assignments.
// @host            localhost:8080
// @BasePath        /
//
// @securityDefinitions.apikey  BearerAuth
// @in                          header
// @name                        Authorization
// @description                 Enter your JWT token as: Bearer <token>
// @bearerFormat                JWT
package main

import (
	"bytes"
	"fmt"
	"net/http"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"
	"time"

	_ "api_server/docs"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v4"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

// ScriptResponse holds the stdout/stderr from a Python script
type ScriptResponse struct {
	Output string `json:"output"`
	Error  string `json:"error,omitempty"`
}

// JWT token Secret and helper
var jwtSecret = []byte("your-super-secret-key") // load from env in prod

func generateToken(login string) (string, error) {
	claims := jwt.MapClaims{
		"sub": login,
		"exp": time.Now().Add(24 * time.Hour).Unix(),
		"iat": time.Now().Unix(),
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(jwtSecret)
}

// Middleware for authorization
func AuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		auth := c.GetHeader("Authorization")
		if auth == "" || !strings.HasPrefix(auth, "Bearer ") {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing or invalid Authorization header"})
			return
		}

		tokStr := strings.TrimPrefix(auth, "Bearer ")
		token, err := jwt.Parse(tokStr, func(t *jwt.Token) (interface{}, error) {
			if t.Method != jwt.SigningMethodHS256 {
				return nil, fmt.Errorf("unexpected signing method")
			}
			return jwtSecret, nil
		})
		if err != nil || !token.Valid {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid token"})
			return
		}

		// you can extract claims if needed: c.Set("claims", token.Claims)
		c.Next()
	}
}

// Checking proper loging to not capture JWT
func isLoginSuccess(msg string) bool {
	re := regexp.MustCompile(`^Zalogowano jako (student|nauczyciel|teacher)! ID uzytkownika: \d+$`)
	return re.MatchString(msg)
}

// --- Request DTOs ---

type CreateCourseReq struct {
	Nazwa           string `json:"nazwa" binding:"required"`
	WlascicielLogin string `json:"wlasciciel_login" binding:"required"`
}

type CreateAssignmentReq struct {
	Kurs    string `json:"nazwa_kursu" binding:"required"`
	Zadanie string `json:"nazwa_zadania" binding:"required"`
	Termin  string `json:"termin" binding:"required"` // YYYY-MM-DD
}

type RenameCourseReq struct {
	StaraNazwa string `json:"stara_nazwa" binding:"required"`
	NowaNazwa  string `json:"nowa_nazwa" binding:"required"`
}

type RescheduleAssignmentReq struct {
	Kurs    string `json:"nazwa_kursu" binding:"required"`
	Zadanie string `json:"nazwa_zadania" binding:"required"`
	Termin  string `json:"nowy_termin" binding:"required"` // YYYY-MM-DD
}

type DeleteCourseReq struct {
	Nazwa string `json:"nazwa" binding:"required"`
}

type DeleteAssignmentReq struct {
	Kurs    string `json:"nazwa_kursu" binding:"required"`
	Zadanie string `json:"nazwa_zadania" binding:"required"`
}

type SubmitAssignmentForm struct {
	StudentLogin string `form:"student_login" binding:"required"`
	Kurs         string `form:"nazwa_kursu" binding:"required"`
	Zadanie      string `form:"nazwa_zadania" binding:"required"`
}

type CheckSubmissionQuery struct {
	StudentLogin string `form:"student_login" binding:"required"`
	Kurs         string `form:"nazwa_kursu" binding:"required"`
	Zadanie      string `form:"nazwa_zadania" binding:"required"`
}

type AssignUserReq struct {
	StudentLogin string `json:"student_login" binding:"required"`
	Kurs         string `json:"nazwa_kursu" binding:"required"`
}

type RemoveUserReq = AssignUserReq

type RegisterReq struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
	Role     string `json:"role" binding:"required"`
	Imie     string `json:"imie" binding:"required"`
	Nazwisko string `json:"nazwisko" binding:"required"`
	Klasa    string `json:"klasa,omitempty"`
}

type LoginReq struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
}

// --- helper to invoke Python scripts ---

func runScript(c *gin.Context, script string, args ...string) {
	// ensure script path is correct
	scriptPath := filepath.Join("scripts", script)
	cmd := exec.Command("python", append([]string{scriptPath}, args...)...)
	var out, stderr bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &stderr
	err := cmd.Run()

	resp := ScriptResponse{Output: strings.TrimSpace(out.String())}
	if err != nil {
		resp.Error = strings.TrimSpace(stderr.String())
		c.JSON(http.StatusInternalServerError, resp)
		return
	}
	c.JSON(http.StatusOK, resp)
}

// --- Handlers ---

// @Summary Create course
// @Security BearerAuth
// @Accept json
// @Produce json
// @Param req body CreateCourseReq true "Create course request"
// @Success 200 {object} ScriptResponse
// @Router /kurs [post]
func createCourse(c *gin.Context) {
	var req CreateCourseReq
	if c.ShouldBindJSON(&req) == nil {
		runScript(c, "tworzenie_kursu.py",
			"--nazwa_kursu", req.Nazwa,
			"--wlasciciel_login", req.WlascicielLogin,
		)
	}
}

// @Summary Create assignment
// @Security BearerAuth
// @Accept json
// @Produce json
// @Param req body CreateAssignmentReq true "Create course assingment"
// @Success 200 {object} ScriptResponse
// @Router /zadanie [post]
func createAssignment(c *gin.Context) {
	var req CreateAssignmentReq
	if c.ShouldBindJSON(&req) == nil {
		runScript(c, "tworzenie_zadania.py",
			"--nazwa_kursu", req.Kurs,
			"--nazwa_zadania", req.Zadanie,
			"--termin", req.Termin,
		)
	}
}

// @Summary Rename course
// @Security BearerAuth
// @Accept json
// @Produce json
// @Param req body RenameCourseReq true "Rename course"
// @Success 200 {object} ScriptResponse
// @Router /kurs [put]
func renameCourse(c *gin.Context) {
	var req RenameCourseReq
	if c.ShouldBindJSON(&req) == nil {
		runScript(c, "modyfikacja_kursu.py",
			"--stara_nazwa", req.StaraNazwa,
			"--nowa_nazwa", req.NowaNazwa,
		)
	}
}

// @Summary Reschedule assignment
// @Security BearerAuth
// @Accept json
// @Produce json
// @Param req body RescheduleAssignmentReq true "Reschedule assingment"
// @Success 200 {object} ScriptResponse
// @Router /zadanie [put]
func rescheduleAssignment(c *gin.Context) {
	var req RescheduleAssignmentReq
	if c.ShouldBindJSON(&req) == nil {
		runScript(c, "modyfikacja_zadania.py",
			"--nazwa_kursu", req.Kurs,
			"--nazwa_zadania", req.Zadanie,
			"--nowy_termin", req.Termin,
		)
	}
}

// @Summary Delete course
// @Security BearerAuth
// @Accept json
// @Produce json
// @Param req body DeleteCourseReq true "Delete course"
// @Success 200 {object} ScriptResponse
// @Router /kurs [delete]
func deleteCourse(c *gin.Context) {
	var req DeleteCourseReq
	if c.ShouldBindJSON(&req) == nil {
		runScript(c, "usuwanie_kursu.py",
			"--nazwa", req.Nazwa,
		)
	}
}

// @Summary Delete assignment
// @Security BearerAuth
// @Accept json
// @Produce json
// @Param req body DeleteAssignmentReq true "Delete assingment"
// @Success 200 {object} ScriptResponse
// @Router /zadanie [delete]
func deleteAssignment(c *gin.Context) {
	var req DeleteAssignmentReq
	if c.ShouldBindJSON(&req) == nil {
		runScript(c, "usuwanie_zadania.py",
			"--nazwa_kursu", req.Kurs,
			"--nazwa_zadania", req.Zadanie,
		)
	}
}

// @Summary Submit assignment
// @Security BearerAuth
// @Accept multipart/form-data
// @Produce json
// @Param student_login formData string true "Student login"
// @Param nazwa_kursu formData string true "Course name"
// @Param nazwa_zadania formData string true "Assignment name"
// @Param plik formData file true "Assignment file"
// @Success 200 {object} ScriptResponse
// @Router /zadanie/upload [post]
func submitAssignment(c *gin.Context) {
	var form SubmitAssignmentForm
	if c.ShouldBind(&form) == nil {
		file, err := c.FormFile("plik")
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "plik is required"})
			return
		}
		dst := filepath.Join("/tmp", file.Filename)
		if err := c.SaveUploadedFile(file, dst); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "save error"})
			return
		}
		runScript(c, "wysylanie_zadania.py",
			"--sciezka_pliku", dst,
			"--student_login", form.StudentLogin,
			"--nazwa_kursu", form.Kurs,
			"--nazwa_zadania", form.Zadanie,
		)
	}
}

// @Summary Check submission
// @Security BearerAuth
// @Accept json
// @Produce json
// @Param student_login query string true "Student login"
// @Param nazwa_kursu query string true "Course name"
// @Param nazwa_zadania query string true "Assignment name"
// @Success 200 {object} ScriptResponse
// @Router /zadanie/check [get]
func checkSubmission(c *gin.Context) {
	var q CheckSubmissionQuery
	if c.ShouldBindQuery(&q) == nil {
		runScript(c, "sprawdz_plik.py",
			"--student_login", q.StudentLogin,
			"--nazwa_kursu", q.Kurs,
			"--nazwa_zadania", q.Zadanie,
		)
	}
}

// @Summary Assign user to course
// @Security BearerAuth
// @Accept json
// @Produce json
// @Param req body AssignUserReq true "Assign user"
// @Success 200 {object} ScriptResponse
// @Router /kurs/assign [post]
func assignUserToCourse(c *gin.Context) {
	var req AssignUserReq
	if c.ShouldBindJSON(&req) == nil {
		runScript(c, "przypisz_uzytkownika_do_kursu.py",
			"--student_login", req.StudentLogin,
			"--nazwa_kursu", req.Kurs,
		)
	}
}

// @Summary Remove user from course
// @Security BearerAuth
// @Accept json
// @Produce json
// @Param req body RemoveUserReq true "Remove user"
// @Success 200 {object} ScriptResponse
// @Router /kurs/remove [delete]
func removeUserFromCourse(c *gin.Context) {
	var req RemoveUserReq
	if c.ShouldBindJSON(&req) == nil {
		runScript(c, "usun_uzytkownika_z_kursu.py",
			"--student_login", req.StudentLogin,
			"--nazwa_kursu", req.Kurs,
		)
	}
}

// @Summary Who am I
// @Security BearerAuth
// @Accept json
// @Produce json
// @Param login query string true "User login"
// @Success 200 {object} ScriptResponse
// @Router /whoami [get]
func whoAmI(c *gin.Context) {
	login := c.Query("login")
	if login == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "login is required"})
		return
	}
	runScript(c, "kim_jestem.py", "--login", login)
}

// @Summary List all tables
// @Security BearerAuth
// @Produce json
// @Success 200 {object} map[string]interface{}
// @Router /all [get]
func listAll(c *gin.Context) {
	// run the Python script and capture stdout
	scriptPath := filepath.Join("scripts", "select_all.py")
	cmd := exec.Command("python", scriptPath)
	out, err := cmd.Output()
	if err != nil {
		// if Python errors, capture stderr and return 500
		buf := &bytes.Buffer{}
		cmd.Stderr = buf
		_ = cmd.Run()
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": strings.TrimSpace(buf.String()),
		})
		return
	}
	// write raw JSON back to client
	c.Data(http.StatusOK, "application/json; charset=utf-8", out)
}

// @Summary Register user
// @Accept json
// @Produce json
// @Param req body RegisterReq true "Register user"
// @Success 200 {object} ScriptResponse
// @Router /register [post]
func registerUser(c *gin.Context) {
	var req RegisterReq
	if c.ShouldBindJSON(&req) == nil {
		args := []string{
			"--email", req.Email,
			"--password", req.Password,
			"--role", req.Role,
			"--imie", req.Imie,
			"--nazwisko", req.Nazwisko,
		}
		if req.Klasa != "" {
			args = append(args, "--klasa", req.Klasa)
		}
		runScript(c, "auth.py", append([]string{"register"}, args...)...)
	}
}

// @Summary Login user
// @Accept json
// @Produce json
// @Param req body LoginReq true "Login user"
// @Success 200 {object} map[string]string
// @Router /login [post]
func loginUser(c *gin.Context) {
	var req LoginReq
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	out, err := exec.Command("python", "scripts/auth.py", "login",
		"--email", req.Email, "--password", req.Password,
	).CombinedOutput()
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": strings.TrimSpace(string(out))})
		return
	}

	// on success, issue JWT
	if isLoginSuccess(strings.TrimSpace(string(out))) {
		token, err := generateToken(req.Email)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "could not generate token"})
			return
		}

		c.JSON(http.StatusOK, gin.H{
			"message": strings.TrimSpace(string(out)),
			"token":   token,
		})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"message": strings.TrimSpace(string(out)),
		})
	}
}

func main() {
	r := gin.Default()
	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	// public
	r.POST("/register", registerUser)
	r.POST("/login", loginUser)

	// protected
	auth := r.Group("/", AuthMiddleware())
	{
		auth.POST("/kurs", createCourse)
		auth.PUT("/kurs", renameCourse)
		auth.DELETE("/kurs", deleteCourse)
		auth.POST("/kurs/assign", assignUserToCourse)
		auth.POST("/kurs/remove", removeUserFromCourse)

		auth.POST("/zadanie", createAssignment)
		auth.PUT("/zadanie", rescheduleAssignment)
		auth.DELETE("/zadanie", deleteAssignment)
		auth.POST("/zadanie/upload", submitAssignment)
		auth.GET("/zadanie/check", checkSubmission)

		auth.GET("/whoami", whoAmI)
		auth.GET("/all", listAll)
	}

	r.Run(":8080")
}
