#include <Python.h>
#include <c_input.h>

void disable(void);



static c_input c_input_;
pythonreutrn init_user_input
()
{
  c_input_ = gen_c_input();
  set_c_keyboard_press(c_input_.keyboard, SDL_SCANCODE_ENTER, disable);
}
pythonreturn get_user_input_events
()
{
  handle_c_input(&c_input_);
}

void disable(void)
{
  
}
