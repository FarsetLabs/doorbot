from doorbot.app import app
import views

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3667, debug=True, use_debugger=True) # T9 code for door
