#!/bin/bash
set -e

RUNZSH=no CHSH=no sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# 修改 ~/.zshrc 中的 plugins 配置。
sed -i 's/plugins=(git)/plugins=(git\n    zsh-autosuggestions\n    zsh-syntax-highlighting\n)/' ~/.zshrc

# 将 ZSH 主题从 robbyrussell 改为 agnoster。
sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/' ~/.zshrc

# 关闭 oh-my-zsh 自动更新。
sed -i 's/^# zstyle '"'"':omz:update'"'"' mode disabled/zstyle '"'"':omz:update'"'"' mode disabled/' ~/.zshrc

# 修改 agnoster 主题添加时间显示
sed -i '/local -a symbols/a\
  symbols+="%D{%H:%M:%S}"' ~/.oh-my-zsh/themes/agnoster.zsh-theme

# 在 ~/.zshrc 文件末尾添加别名配置。
cat >> ~/.zshrc << 'EOF'

# 自定义别名配置。
alias cp='cp -i'
alias mv='mv -i'
alias vi="/usr/bin/vim"
alias ll="clear;ls -aihl --color=tty --time-style=long-iso"
alias rm="/bin/rm -i"
alias sudo='sudo '
EOF