<h1>DISKO 1</h1>

Author: Darkaicg492

<img width="631" height="522" alt="image" src="https://github.com/user-attachments/assets/c7d0b544-8777-4afb-9b2d-44443285ceca" />

After extracting the disk image. This challenge can simply be solved by parsing strings applied to the .dd file into a grep for the word "pico"

`picoCTF{1t5_ju5t_4_5tr1n9_c63b02ef}`


To tie off the curiosity.

I was able to mount the .dd file and view its contents using the kpartx utility. This handles a lot of the loop device setup and file mounting offset. by typing `kpartx -av disko-1.dd` I assigned an available loop device. Then, I used `losetup -l` so see which was assigned. Lastly, I created a new mount directory and then mounted this loop to the directory using `sudo mount -o loop /dev/loop0 /mnt/mount-pico`.

<img width="651" height="622" alt="image" src="https://github.com/user-attachments/assets/40b4120d-fdd8-4fc7-8f75-5bc7b8f3aa70" />

Unfortunately due to the large number of files in this directory, Its not obvious which one has the flag - thus, the use of strings and grep was appropriate. 
