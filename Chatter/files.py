class msrgb565:
  def write(filename, sprite, width_length, width, height_length, height, transparent):
    with open(filename+'.rgb565','wb') as f:
      f.write(
        bytearray(b'MSRGB565')+
        width_length.to_bytes(2,'big')+
        width.to_bytes(width_length,'big')+
        height_length.to_bytes(2,'big')+
        height.to_bytes(height_length,'big')+
        transparent.to_bytes(2,'big')+
        sprite
      )
  def read(filename):
    with open(filename+'.rgb565', 'rb') as f:
      f.seek(8)
      _width_length = int.from_bytes(f.read(2), 'big')
      _rwidth = int.from_bytes(f.read(_width_length), 'big')
      _height_length = int.from_bytes(f.read(2), 'big')
      _rheight = int.from_bytes(f.read(_height_length), 'big')
      _rtrans = int.from_bytes(f.read(2), 'big')
      _rsprite = bytearray(f.read())
    return _rwidth, _rheight, _rtrans, _rsprite

class msmono:
  def write(filename, sprite, width_length, width, height_length, height):
    with open(filename+'.mhlsb','wb') as f:
      f.write(
        bytearray(b'MSMONO')+
        width_length.to_bytes(2,'big')+
        width.to_bytes(width_length,'big')+
        height_length.to_bytes(2,'big')+
        height.to_bytes(height_length,'big')+
        sprite
      )
  def read(filename):
    with open(filename+'.mhlsb', 'rb') as f:
      f.seek(6)
      _width_length = int.from_bytes(f.read(2), 'big')
      _rwidth = int.from_bytes(f.read(_width_length), 'big')
      _height_length = int.from_bytes(f.read(2), 'big')
      _rheight = int.from_bytes(f.read(_height_length), 'big')
      _rsprite = bytearray(f.read())
    return _rwidth, _rheight, _rsprite
